# AAC System - Module 2: The Brain (Knowledge Management)

## Overview
Capture → Organize → Connect → Remember

## Components

### 1. Knowledge Capture
- **Input Types:**
  - Notes (text)
  - Voice transcripts (audio → text)
  - Web clips (URL → extracted content)
  - Code snippets
  - PDF extracts

- **Domains:**
  - Tech - Programming, infrastructure, tools
  - DND - Game rules, campaigns, characters
  - Masters - Academic research, coursework
  - Life - Personal wisdom, decisions
  - Finance - Investment knowledge, strategies
  - Health - Medical notes, protocols

### 2. Anki Integration (Spaced Repetition)
```python
class AnkiManager:
    def create_card(self, knowledge_entry):
        """Create Anki flashcard from knowledge"""
        card = {
            'front': extract_front(knowledge_entry.content),
            'back': extract_back(knowledge_entry.content),
            'tags': knowledge_entry.tags + ['auto'],
            'deck': f'Nexus::{knowledge_entry.domain}'
        }
        return anki.create_card(card)
    
    def sync_cards(self):
        """Sync with AnkiWeb for review on mobile"""
        return anki.sync()
```

### 3. Vector Embeddings (Qdrant)
```python
class VectorStore:
    def embed_and_store(self, entry):
        """Generate embedding and store in Qdrant"""
        embedding = model.encode(entry.content)
        qdrant_id = qdrant.upsert(
            collection='knowledge',
            vector=embedding,
            payload={
                'id': entry.id,
                'title': entry.title,
                'domain': entry.domain,
                'owner': entry.owner
            }
        )
        return qdrant_id
```

### 4. Knowledge Graph
```python
class KnowledgeGraph:
    def connect_entries(self, entry_id, related_ids):
        """Create connections between knowledge entries"""
        # Stores as relationships in graph
        return graph.add_edges(entry_id, related_ids)
    
    def find_related(self, entry_id, max_depth=2):
        """Find related knowledge via graph traversal"""
        return graph.bfs(entry_id, max_depth)
```

## API Endpoints

```
POST /api/v1/brain/entries
  - Create knowledge entry
  - Auto-generate embedding
  - Optionally create Anki card

GET /api/v1/brain/entries
  - List entries (with filters)

GET /api/v1/brain/entries/{id}
  - Get single entry with connections

POST /api/v1/brain/entries/{id}/anki
  - Create Anki card from entry

POST /api/v1/brain/entries/{id}/connect
  - Connect to other entries

GET /api/v1/brain/search
  - Semantic search via Qdrant
  - Returns related entries

POST /api/v1/brain/sync/ankiw
  - Trigger AnkiWeb sync

POST /api/v1/brain/sync/embeddings
  - Re-generate embeddings
```

## Data Model

### Knowledge Entry
```python
{
    "id": "knl_xxxxxxxx",
    "timestamp": "2026-02-18T10:30:00Z",
    "owner": "faza",
    "title": "Docker container networking",
    "content": "...",
    "content_type": "note",
    "domain": "tech",
    "project": "aac-infrastructure",
    "tags": ["docker", "networking", "cloudflare"],
    "is_srs_eligible": true,
    "srs_card_id": "anki_card_123",
    "qdrant_id": "vector_456",
    "embedding_synced": true
}
```

## Implementation Plan

### Week 1: Foundation
- [x] Database schema (knowledge_entries, worktrees)
- [ ] BrainModule class (CRUD operations)
- [ ] Vector embedding generation
- [ ] Qdrant integration

### Week 2: Anki Integration
- [ ] Anki Connect API integration
- [ ] Auto-card generation rules
- [ ] Sync with AnkiWeb

### Week 3: Search & Graph
- [ ] Semantic search via Qdrant
- [ ] Knowledge graph connections
- [ ] Related entries discovery

### Week 4: Capture Automation
- [ ] Voice transcript integration (audio → text)
- [ ] Web clipper (URL → content extraction)
- [ ] Code snippet parser

## File Structure

```
modules/brain/
├── __init__.py
├── models.py          # Dataclass models
├── service.py         # Business logic
├── api.py            # FastAPI routes
├── anki.py           # Anki integration
├── embeddings.py     # Vector generation
├── graph.py          # Knowledge graph
└── search.py         # Semantic search
```

## Dependencies

- **Qdrant:** Vector store (already running in AAC stack)
- **AnkiConnect:** Local API for Anki desktop
- **Sentence Transformers:** Vector embedding generation
- **BeautifulSoup4:** Web content extraction

## Quick Start

```bash
# Install dependencies
pip install sentence-transformers beautifulsoup4

# Start Anki with AnkiConnect plugin
# (Plugin: https://github.com/FooSoft/anki-connect)

# Create a knowledge entry
curl -X POST http://localhost:8000/api/v1/brain/entries \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Docker networking basics",
    "content": "Containers use bridge networks by default...",
    "domain": "tech",
    "project": "aac-infrastructure",
    "tags": ["docker", "networking"]
  }'
```
