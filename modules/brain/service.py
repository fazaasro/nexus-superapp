"""
Module 2: The Brain (Knowledge Management)
Knowledge capture, organization, Anki integration, vector embeddings
"""
import json
import re
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.database import get_db, generate_uuid, log_audit


class BrainModule:
    """Knowledge management module"""
    
    DOMAINS = ['tech', 'dnd', 'masters', 'life', 'finance', 'health']
    CONTENT_TYPES = ['note', 'voice_transcript', 'web_clip', 'code', 'pdf_extract']
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "data" / "levy.db"
    
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
    
    def _queue_embedding_generation(self, entry_id: str):
        """Queue embedding generation (async placeholder)"""
        # TODO: Implement async queue for embedding generation
        # For now, we'll generate synchronously if requested
        pass
    
    def generate_embedding(self, entry_id: str) -> Dict:
        """Generate vector embedding for a knowledge entry"""
        entry = self.get_entry(entry_id, 'system')  # System user
        
        if not entry:
            return {'error': 'Entry not found'}
        
        # Generate embedding (placeholder - need sentence-transformers)
        # TODO: Integrate sentence-transformers
        embedding = self._generate_embedding_vector(entry['content'])
        
        # Store in Qdrant (placeholder)
        # TODO: Integrate Qdrant client
        qdrant_id = self._store_embedding(entry_id, embedding, entry)
        
        # Update database
        with get_db() as conn:
            conn.execute(
                "UPDATE knowledge_entries SET qdrant_id = ?, embedding_synced = 1 WHERE id = ?",
                (qdrant_id, entry_id)
            )
        
        return {'entry_id': entry_id, 'qdrant_id': qdrant_id, 'status': 'embedded'}
    
    def _generate_embedding_vector(self, text: str) -> List[float]:
        """Generate embedding vector from text (placeholder)"""
        # TODO: Implement with sentence-transformers
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # return model.encode(text).tolist()
        return [0.0] * 384  # Placeholder: 384-dimensional vector
    
    def _store_embedding(self, entry_id: str, embedding: List[float], entry: Dict) -> str:
        """Store embedding in Qdrant (placeholder)"""
        # TODO: Implement Qdrant integration
        # qdrant.upsert(
        #     collection='knowledge',
        #     points=[{
        #         'id': entry_id,
        #         'vector': embedding,
        #         'payload': {
        #             'title': entry['title'],
        #             'domain': entry.get('domain'),
        #             'owner': entry['owner']
        #         }
        #     }]
        # )
        return f"qdrant_{entry_id}"
    
    def _delete_embedding(self, entry_id: str):
        """Delete embedding from Qdrant (placeholder)"""
        # TODO: Implement Qdrant deletion
        pass
    
    # ========== ANKI INTEGRATION ==========
    
    def create_anki_card(self, entry_id: str, user_id: str) -> Dict:
        """Create Anki card from knowledge entry"""
        entry = self.get_entry(entry_id, user_id)
        
        if not entry:
            return {'error': 'Entry not found'}
        
        # Generate front/back from content
        front, back = self._extract_anki_content(entry['content'])
        
        # Create card via AnkiConnect (placeholder)
        # TODO: Implement AnkiConnect integration
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
        """Create card via AnkiConnect API (placeholder)"""
        # TODO: Implement AnkiConnect integration
        # import requests
        # response = requests.post('http://localhost:8765', json={
        #     'action': 'addNote',
        #     'version': 6,
        #     'params': {
        #         'note': {
        #             'deckName': card_data['deck'],
        #             'modelName': 'Basic',
        #             'fields': {'Front': card_data['front'], 'Back': card_data['back']},
        #             'tags': card_data['tags']
        #         }
        #     }
        # })
        # return response.json()['result']
        return f"anki_card_{generate_uuid()}"
    
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
        """Extract content from web page (placeholder)"""
        # TODO: Implement with beautifulsoup4
        # import requests
        # from bs4 import BeautifulSoup
        #
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        #
        # # Extract title
        # title = soup.find('title').text if soup.find('title') else url
        #
        # # Extract main content
        # content = ''
        # for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
        #     content += tag.get_text() + '\n'
        #
        # return {'title': title, 'content': content.strip()}
        return None
    
    # ========== KNOWLEDGE GRAPH ==========
    
    def _get_related_entries(self, entry_id: str, user_id: str, max_depth: int = 2) -> List[Dict]:
        """Get related knowledge entries via graph traversal (placeholder)"""
        # TODO: Implement knowledge graph with networkx
        # For now, return empty list
        return []
    
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
        """Search knowledge entries (keyword search for now)"""
        filters = filters or {}
        
        # Basic keyword search
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
        
        results = []
        for row in rows:
            entry = dict(row)
            if entry.get('tags'):
                entry['tags'] = json.loads(entry['tags'])
            results.append(entry)
        
        # TODO: Add semantic search via Qdrant
        # if filters.get('semantic'):
        #     results.extend(self._semantic_search(query, user_id, filters))
        
        return results
    
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
