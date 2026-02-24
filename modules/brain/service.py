"""
Module 2: The Brain (Knowledge Management)
Knowledge capture, organization, Anki integration, vector embeddings
"""
import json
import re
import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import networkx as nx
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from core.database import get_db, generate_uuid, log_audit


class BrainModule:
    """Knowledge management module"""

    DOMAINS = ['tech', 'dnd', 'masters', 'life', 'finance', 'health']
    CONTENT_TYPES = ['note', 'voice_transcript', 'web_clip', 'code', 'pdf_extract']

    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"

        # Initialize Qdrant client
        qdrant_host = os.getenv("QDRANT_HOST", "http://127.0.0.1:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant = QdrantClient(url=qdrant_host, api_key=qdrant_api_key)
        self.collection_name = os.getenv("QDRANT_KNOWLEDGE_COLLECTION", "nexus_knowledge")

        # Initialize sentence transformer model (lazy loading)
        self._embedding_model = None

        # Initialize AnkiConnect URL
        self.anki_url = os.getenv("ANKICONNECT_URL", "http://127.0.0.1:8765")

        # Initialize knowledge graph
        self.knowledge_graph = nx.DiGraph()

        # Ensure Qdrant collection exists
        self._ensure_collection_exists()

    @property
    def embedding_model(self):
        """Lazy load sentence transformer model"""
        if self._embedding_model is None:
            logger.info("Loading sentence transformer model...")
            self._embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded")
        return self._embedding_model

    # ========== KNOWLEDGE ENTRY CRUD ==========

    def create_entry(self, data: Dict, user_id: str) -> Dict:
        """Create a new knowledge entry"""
        entry_id = f"knl_{generate_uuid()}"

        with get_db() as conn:
            conn.execute(
                """INSERT INTO knowledge_entries
                   (id, owner, created_by, title, content, content_type, source_url,
                    source_file, domain, project, tags, is_srs_eligible)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    entry_id,
                    data.get('owner', user_id),
                    user_id,
                    data['title'],
                    data['content'],
                    data.get('content_type', 'note'),
                    data.get('source_url'),
                    data.get('source_file'),
                    data.get('domain'),
                    data.get('project'),
                    json.dumps(data.get('tags', [])),
                    data.get('is_srs_eligible', False)
                )
            )

        # Audit log
        log_audit(user_id, 'brain', 'create', 'knowledge_entry', entry_id,
                 {'title': data['title'], 'domain': data.get('domain')})

        # Auto-generate embedding (async)
        self._queue_embedding_generation(entry_id)

        return {'id': entry_id, 'status': 'created'}

    def get_entries(self, user_id: str, include_shared: bool = True,
                    domain: str = None, project: str = None,
                    content_type: str = None, limit: int = 50) -> List[Dict]:
        """Get knowledge entries for user"""
        owners = [user_id]
        if include_shared:
            owners.append('shared')

        query = "SELECT * FROM knowledge_entries WHERE owner IN ({})".format(
            ','.join(['?' for _ in owners])
        )
        params = owners.copy()

        if domain:
            query += " AND domain = ?"
            params.append(domain)

        if project:
            query += " AND project = ?"
            params.append(project)

        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with get_db() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

        entries = []
        for row in rows:
            entry = dict(row)
            if entry.get('tags'):
                entry['tags'] = json.loads(entry['tags'])
            entries.append(entry)

        return entries

    def get_entry(self, entry_id: str, user_id: str) -> Optional[Dict]:
        """Get a single knowledge entry by ID"""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM knowledge_entries WHERE id = ?",
                (entry_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            entry = dict(row)
            if entry.get('tags'):
                entry['tags'] = json.loads(entry['tags'])

            # Get related entries (knowledge graph)
            entry['related'] = self._get_related_entries(entry_id, user_id)

            return entry

    def update_entry(self, entry_id: str, data: Dict, user_id: str) -> Dict:
        """Update a knowledge entry"""
        update_fields = []
        params = []

        for field in ['title', 'content', 'domain', 'project', 'is_srs_eligible']:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])

        if 'tags' in data:
            update_fields.append("tags = ?")
            params.append(json.dumps(data['tags']))

        if not update_fields:
            return {'error': 'No fields to update'}

        params.append(entry_id)

        with get_db() as conn:
            conn.execute(
                f"UPDATE knowledge_entries SET {', '.join(update_fields)} WHERE id = ?",
                params
            )

        log_audit(user_id, 'brain', 'update', 'knowledge_entry', entry_id, data)

        return {'id': entry_id, 'status': 'updated'}

    def delete_entry(self, entry_id: str, user_id: str) -> Dict:
        """Delete a knowledge entry"""
        with get_db() as conn:
            # Check ownership
            entry = conn.execute(
                "SELECT owner FROM knowledge_entries WHERE id = ?",
                (entry_id,)
            ).fetchone()

            if not entry:
                return {'error': 'Entry not found'}

            if entry['owner'] not in [user_id, 'shared']:
                return {'error': 'Permission denied'}

            conn.execute(
                "DELETE FROM knowledge_entries WHERE id = ?",
                (entry_id,)
            )

        log_audit(user_id, 'brain', 'delete', 'knowledge_entry', entry_id, {})

        # Delete from Qdrant (if embedding exists)
        self._delete_embedding(entry_id)

        return {'id': entry_id, 'status': 'deleted'}

    # ========== EMBEDDINGS (Qdrant) ==========

    def _ensure_collection_exists(self):
        """Ensure Qdrant collection exists"""
        try:
            collections = self.qdrant.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                logger.info(f"Creating Qdrant collection: {self.collection_name}")
                self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection exists: {e}")

    def _queue_embedding_generation(self, entry_id: str):
        """Queue embedding generation (async placeholder)"""
        # Generate embedding synchronously for now
        # In production, use celery/rq for async processing
        try:
            self.generate_embedding(entry_id)
        except Exception as e:
            logger.error(f"Error generating embedding for {entry_id}: {e}")

    def generate_embedding(self, entry_id: str) -> Dict:
        """Generate vector embedding for a knowledge entry"""
        entry = self.get_entry(entry_id, 'system')  # System user

        if not entry:
            return {'error': 'Entry not found'}

        # Generate embedding with sentence-transformers
        embedding = self._generate_embedding_vector(entry['content'])

        # Store in Qdrant
        qdrant_id = self._store_embedding(entry_id, embedding, entry)

        # Update database
        with get_db() as conn:
            conn.execute(
                "UPDATE knowledge_entries SET qdrant_id = ?, embedding_synced = 1 WHERE id = ?",
                (qdrant_id, entry_id)
            )

        return {'entry_id': entry_id, 'qdrant_id': qdrant_id, 'status': 'embedded'}

    def _generate_embedding_vector(self, text: str) -> List[float]:
        """Generate embedding vector from text using sentence-transformers"""
        try:
            # Use the lazy-loaded embedding model
            embedding = self.embedding_model.encode(text, convert_to_numpy=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 384

    def _store_embedding(self, entry_id: str, embedding: List[float], entry: Dict) -> str:
        """Store embedding in Qdrant"""
        try:
            point = PointStruct(
                id=entry_id,
                vector=embedding,
                payload={
                    'title': entry['title'],
                    'domain': entry.get('domain'),
                    'owner': entry['owner'],
                    'content_type': entry.get('content_type'),
                    'timestamp': entry.get('timestamp')
                }
            )

            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Stored embedding for {entry_id} in Qdrant")
            return entry_id
        except Exception as e:
            logger.error(f"Error storing embedding in Qdrant: {e}")
            return entry_id

    def _delete_embedding(self, entry_id: str):
        """Delete embedding from Qdrant"""
        try:
            self.qdrant.delete(
                collection_name=self.collection_name,
                points_selector=entry_id
            )
            logger.info(f"Deleted embedding for {entry_id} from Qdrant")
        except Exception as e:
            logger.error(f"Error deleting embedding from Qdrant: {e}")

    # ========== ANKI INTEGRATION ==========

    def create_anki_card(self, entry_id: str, user_id: str) -> Dict:
        """Create Anki card from knowledge entry"""
        entry = self.get_entry(entry_id, user_id)

        if not entry:
            return {'error': 'Entry not found'}

        # Generate front/back from content
        front, back = self._extract_anki_content(entry['content'])

        # Create card via AnkiConnect API
        card_id = self._create_anki_card_via_api({
            'deck': f"Nexus::{entry.get('domain', 'General')}",
            'front': front,
            'back': back,
            'tags': entry.get('tags', []) + ['nexus', 'auto']
        })

        # Update entry
        with get_db() as conn:
            conn.execute(
                "UPDATE knowledge_entries SET srs_card_id = ? WHERE id = ?",
                (card_id, entry_id)
            )

        log_audit(user_id, 'brain', 'create', 'anki_card', card_id,
                 {'entry_id': entry_id})

        return {'entry_id': entry_id, 'anki_card_id': card_id, 'status': 'created'}

    def _extract_anki_content(self, content: str) -> tuple:
        """Extract front/back content for Anki card"""
        # Look for Q: / A: pattern
        qa_match = re.search(r'Q:\s*(.+?)\s*\n\s*A:\s*(.+)', content, re.DOTALL)

        if qa_match:
            front = qa_match.group(1).strip()
            back = qa_match.group(2).strip()
        else:
            # Fallback: first paragraph = front, rest = back
            paragraphs = content.split('\n\n')
            front = paragraphs[0].strip()[:200]  # Limit length
            back = '\n\n'.join(paragraphs[1:]).strip()

        return front, back

    def _create_anki_card_via_api(self, card_data: Dict) -> str:
        """Create card via AnkiConnect API"""
        try:
            response = requests.post(
                self.anki_url,
                json={
                    'action': 'addNote',
                    'version': 6,
                    'params': {
                        'note': {
                            'deckName': card_data['deck'],
                            'modelName': 'Basic',
                            'fields': {
                                'Front': card_data['front'],
                                'Back': card_data['back']
                            },
                            'tags': card_data['tags']
                        }
                    }
                },
                timeout=10
            )

            result = response.json()

            if result.get('error'):
                logger.error(f"AnkiConnect error: {result['error']}")
                return None

            logger.info(f"Created Anki card: {result['result']}")
            return result['result']

        except Exception as e:
            logger.error(f"Error creating Anki card: {e}")
            return None

    # ========== WEB CLIPPING ==========

    def create_web_clip(self, url: str, user_id: str, metadata: Dict = None) -> Dict:
        """Clip a web page as knowledge entry"""
        # Extract content from URL
        content_data = self._extract_web_content(url)

        if not content_data:
            return {'error': 'Failed to extract content from URL'}

        # Create entry
        entry_id = f"knl_{generate_uuid()}"

        with get_db() as conn:
            conn.execute(
                """INSERT INTO knowledge_entries
                   (id, owner, created_by, title, content, content_type, source_url,
                    domain, project, tags)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    entry_id,
                    metadata.get('owner', user_id) if metadata else user_id,
                    user_id,
                    metadata.get('title') or content_data.get('title', url),
                    content_data['content'],
                    'web_clip',
                    url,
                    metadata.get('domain'),
                    metadata.get('project'),
                    json.dumps(metadata.get('tags', [])) if metadata else '[]'
                )
            )

        log_audit(user_id, 'brain', 'create', 'web_clip', entry_id,
                 {'url': url, 'title': content_data.get('title')})

        return {'id': entry_id, 'status': 'created', 'title': content_data.get('title')}

    def _extract_web_content(self, url: str) -> Optional[Dict]:
        """Extract content from web page using beautifulsoup4"""
        try:
            # Set user agent to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else url

            # Extract main content (try common content selectors first)
            content = ''

            # Try common article/content containers
            for selector in ['article', 'main', '[role="main"]', '.content', '.article']:
                container = soup.select_one(selector)
                if container:
                    break

            if not container:
                # Fallback to body
                container = soup.find('body')

            if container:
                # Extract text from paragraphs, headings, and lists
                for tag in container.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li']):
                    text = tag.get_text(strip=True)
                    if text:
                        content += text + '\n'

            content = content.strip()

            if not content:
                return None

            logger.info(f"Extracted content from {url}: {len(content)} chars")

            return {'title': title, 'content': content}

        except Exception as e:
            logger.error(f"Error extracting web content from {url}: {e}")
            return None

    # ========== KNOWLEDGE GRAPH ==========

    def _get_related_entries(self, entry_id: str, user_id: str, max_depth: int = 2) -> List[Dict]:
        """Get related knowledge entries via graph traversal using networkx"""
        try:
            # Rebuild graph for user (in production, cache this)
            self._build_knowledge_graph(user_id)

            if entry_id not in self.knowledge_graph:
                return []

            # BFS traversal to find related entries
            related = []
            visited = set([entry_id])

            for depth in range(max_depth):
                if depth == 0:
                    # Get direct neighbors
                    neighbors = list(self.knowledge_graph.neighbors(entry_id))
                else:
                    # Get neighbors of current related entries
                    new_neighbors = []
                    for rel_id in related:
                        if rel_id not in visited:
                            new_neighbors.extend(
                                [n for n in self.knowledge_graph.neighbors(rel_id) if n not in visited]
                            )
                    neighbors = new_neighbors

                # Add neighbors to visited and related
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor != entry_id:
                        visited.add(neighbor)
                        related.append(neighbor)

                if not neighbors:
                    break

            # Fetch entry details
            entries = []
            for rel_id in related[:10]:  # Limit to 10 related entries
                entry = self.get_entry(rel_id, user_id)
                if entry:
                    entries.append(entry)

            return entries

        except Exception as e:
            logger.error(f"Error getting related entries: {e}")
            return []

    def _build_knowledge_graph(self, user_id: str):
        """Build knowledge graph using networkx"""
        try:
            # Clear existing graph
            self.knowledge_graph = nx.DiGraph()

            # Get all entries for user
            entries = self.get_entries(user_id, include_shared=True, limit=1000)

            # Add nodes
            for entry in entries:
                self.knowledge_graph.add_node(
                    entry['id'],
                    title=entry['title'],
                    domain=entry.get('domain'),
                    tags=entry.get('tags', [])
                )

            # Add edges based on:
            # 1. Same domain
            # 2. Common tags
            # 3. Same project
            entries_dict = {e['id']: e for e in entries}

            for i, entry1 in enumerate(entries):
                for entry2 in entries[i+1:]:
                    # Skip self
                    if entry1['id'] == entry2['id']:
                        continue

                    # Calculate similarity score
                    similarity = self._calculate_entry_similarity(entry1, entry2)

                    # Add edge if similarity > threshold
                    if similarity > 0.3:
                        self.knowledge_graph.add_edge(
                            entry1['id'],
                            entry2['id'],
                            weight=similarity
                        )

            logger.info(f"Built knowledge graph: {len(self.knowledge_graph.nodes)} nodes, {len(self.knowledge_graph.edges)} edges")

        except Exception as e:
            logger.error(f"Error building knowledge graph: {e}")

    def _calculate_entry_similarity(self, entry1: Dict, entry2: Dict) -> float:
        """Calculate similarity between two entries"""
        score = 0.0

        # Domain match (30%)
        if entry1.get('domain') and entry2.get('domain'):
            if entry1['domain'] == entry2['domain']:
                score += 0.3

        # Tag overlap (40%)
        tags1 = set(entry1.get('tags', []))
        tags2 = set(entry2.get('tags', []))
        if tags1 and tags2:
            overlap = len(tags1 & tags2)
            total = len(tags1 | tags2)
            if total > 0:
                score += 0.4 * (overlap / total)

        # Project match (30%)
        if entry1.get('project') and entry2.get('project'):
            if entry1['project'] == entry2['project']:
                score += 0.3

        return score

    # ========== WORKTREE MANAGEMENT ==========

    def create_worktree(self, data: Dict, user_id: str) -> Dict:
        """Create a git worktree entry"""
        worktree_id = f"wkt_{generate_uuid()}"

        with get_db() as conn:
            conn.execute(
                """INSERT INTO worktrees
                   (id, owner, repo_name, branch_name, worktree_path, status, context_notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    worktree_id,
                    data.get('owner', user_id),
                    data['repo_name'],
                    data['branch_name'],
                    data['worktree_path'],
                    'active',
                    data.get('context_notes')
                )
            )

        return {'id': worktree_id, 'status': 'created'}

    def get_worktrees(self, user_id: str, status: str = None) -> List[Dict]:
        """Get worktrees for user"""
        query = "SELECT * FROM worktrees WHERE owner = ?"
        params = [user_id]

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY last_accessed DESC"

        with get_db() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_worktree_access(self, worktree_id: str, user_id: str) -> Dict:
        """Update last access time for worktree"""
        with get_db() as conn:
            conn.execute(
                "UPDATE worktrees SET last_accessed = ? WHERE id = ?",
                (datetime.now().isoformat(), worktree_id)
            )

        return {'id': worktree_id, 'status': 'accessed'}

    # ========== SEARCH ==========

    def search_entries(self, query: str, user_id: str, filters: Dict = None) -> List[Dict]:
        """Search knowledge entries with keyword and semantic search"""
        filters = filters or {}

        # Keyword search (SQL LIKE)
        results = []

        if not filters.get('semantic_only'):
            search_query = """
                SELECT * FROM knowledge_entries
                WHERE owner IN (?, 'shared')
                  AND (title LIKE ? OR content LIKE ?)
            """
            params = [user_id, f"%{query}%", f"%{query}%"]

            if filters.get('domain'):
                search_query += " AND domain = ?"
                params.append(filters['domain'])

            if filters.get('project'):
                search_query += " AND project = ?"
                params.append(filters['project'])

            search_query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(filters.get('limit', 50))

            with get_db() as conn:
                cursor = conn.execute(search_query, params)
                rows = cursor.fetchall()

            for row in rows:
                entry = dict(row)
                if entry.get('tags'):
                    entry['tags'] = json.loads(entry['tags'])
                # Mark as keyword match
                entry['match_type'] = 'keyword'
                results.append(entry)

        # Semantic search via Qdrant (if requested or if keyword search yields few results)
        if filters.get('semantic') or (filters.get('hybrid') and len(results) < 5):
            semantic_results = self._semantic_search(query, user_id, filters)

            # Remove duplicates (by entry ID)
            seen_ids = {r['id'] for r in results}

            for entry in semantic_results:
                if entry['id'] not in seen_ids:
                    entry['match_type'] = 'semantic'
                    results.append(entry)
                    seen_ids.add(entry['id'])

                # Stop if we have enough results
                if len(results) >= filters.get('limit', 50):
                    break

        return results

    def _semantic_search(self, query: str, user_id: str, filters: Dict = None) -> List[Dict]:
        """Semantic search using Qdrant vector embeddings"""
        try:
            filters = filters or {}

            # Generate query embedding
            query_embedding = self._generate_embedding_vector(query)

            # Build Qdrant filter
            qdrant_filter = None

            # Only search for entries owned by user or shared
            # This is done by filtering after retrieval for simplicity
            # In production, use Qdrant's payload filter

            # Search in Qdrant
            search_results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=filters.get('limit', 20),
                score_threshold=0.5  # Minimum similarity score
            )

            # Fetch full entries from database
            entry_ids = [hit.id for hit in search_results]
            if not entry_ids:
                return []

            placeholders = ','.join(['?' for _ in entry_ids])
            db_query = f"SELECT * FROM knowledge_entries WHERE id IN ({placeholders}) AND owner IN (?, 'shared')"
            db_params = entry_ids + [user_id]

            with get_db() as conn:
                cursor = conn.execute(db_query, db_params)
                rows = cursor.fetchall()

            # Build results map for quick lookup
            entries_map = {row['id']: dict(row) for row in rows}

            # Combine with Qdrant scores
            results = []
            for hit in search_results:
                if hit.id in entries_map:
                    entry = entries_map[hit.id]
                    if entry.get('tags'):
                        entry['tags'] = json.loads(entry['tags'])
                    entry['similarity_score'] = hit.score
                    results.append(entry)

            # Sort by similarity score (descending)
            results.sort(key=lambda x: x['similarity_score'], reverse=True)

            logger.info(f"Semantic search for '{query}': {len(results)} results")

            return results

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []

    # ========== STATISTICS ==========

    def get_stats(self, user_id: str) -> Dict:
        """Get knowledge statistics for user"""
        with get_db() as conn:
            # Total entries
            total = conn.execute(
                "SELECT COUNT(*) as count FROM knowledge_entries WHERE owner IN (?, 'shared')",
                (user_id,)
            ).fetchone()['count']

            # Entries by domain
            by_domain = conn.execute(
                """SELECT domain, COUNT(*) as count
                   FROM knowledge_entries
                   WHERE owner IN (?, 'shared')
                   GROUP BY domain""",
                (user_id,)
            ).fetchall()

            # SRS cards created
            srs_count = conn.execute(
                """SELECT COUNT(*) as count
                   FROM knowledge_entries
                   WHERE owner IN (?, 'shared') AND srs_card_id IS NOT NULL""",
                (user_id,)
            ).fetchone()['count']

            # Entries synced to Qdrant
            synced_count = conn.execute(
                """SELECT COUNT(*) as count
                   FROM knowledge_entries
                   WHERE owner IN (?, 'shared') AND embedding_synced = 1""",
                (user_id,)
            ).fetchone()['count']

            return {
                'total_entries': total,
                'entries_by_domain': {row['domain']: row['count'] for row in by_domain},
                'srs_cards_created': srs_count,
                'entries_with_embeddings': synced_count
            }

    def _trigger_anki_sync(self) -> Dict:
        """Trigger AnkiConnect to sync with AnkiWeb"""
        try:
            response = requests.post(
                self.anki_url,
                json={
                    'action': 'sync',
                    'version': 6
                },
                timeout=30
            )

            result = response.json()

            if result.get('error'):
                logger.error(f"AnkiConnect sync error: {result['error']}")
                return {'error': result['error']}

            logger.info("AnkiWeb sync triggered successfully")
            return result

        except Exception as e:
            logger.error(f"Error triggering AnkiWeb sync: {e}")
            return {'error': str(e)}
