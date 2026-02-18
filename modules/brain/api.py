"""
API routes for The Brain module (Knowledge Management)
FastAPI endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

from .service import BrainModule


router = APIRouter(prefix="/api/v1/brain", tags=["brain"])
brain = BrainModule()


# ========== KNOWLEDGE ENTRY ENDPOINTS ==========

@router.post("/entries")
async def create_entry(entry_data: dict):
    """Create a new knowledge entry"""
    try:
        result = brain.create_entry(entry_data, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/entries")
async def list_entries(
    domain: Optional[str] = None,
    project: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = Query(50, le=200)
):
    """List knowledge entries"""
    try:
        entries = brain.get_entries(
            user_id='faza',  # TODO: Get from auth
            domain=domain,
            project=project,
            content_type=content_type,
            limit=limit
        )
        return {'entries': entries, 'count': len(entries)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/entries/{entry_id}")
async def get_entry(entry_id: str):
    """Get a single knowledge entry"""
    try:
        entry = brain.get_entry(entry_id, user_id='faza')  # TODO: Get from auth
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/entries/{entry_id}")
async def update_entry(entry_id: str, update_data: dict):
    """Update a knowledge entry"""
    try:
        result = brain.update_entry(entry_id, update_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete a knowledge entry"""
    try:
        result = brain.delete_entry(entry_id, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== ANKI INTEGRATION ==========

@router.post("/entries/{entry_id}/anki")
async def create_anki_card(entry_id: str):
    """Create Anki card from knowledge entry"""
    try:
        result = brain.create_anki_card(entry_id, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== WEB CLIPPING ==========

@router.post("/clip")
async def create_web_clip(url_data: dict):
    """Clip a web page as knowledge entry"""
    try:
        url = url_data.get('url')
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        result = brain.create_web_clip(url, user_id='faza', metadata=url_data)  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== WORKTREE MANAGEMENT ==========

@router.post("/worktrees")
async def create_worktree(worktree_data: dict):
    """Create a git worktree entry"""
    try:
        result = brain.create_worktree(worktree_data, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/worktrees")
async def list_worktrees(status: Optional[str] = None):
    """List worktrees"""
    try:
        worktrees = brain.get_worktrees(user_id='faza', status=status)  # TODO: Get from auth
        return {'worktrees': worktrees, 'count': len(worktrees)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/worktrees/{worktree_id}/access")
async def update_worktree_access(worktree_id: str):
    """Update last access time for worktree"""
    try:
        result = brain.update_worktree_access(worktree_id, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== SEARCH ==========

@router.get("/search")
async def search_entries(
    q: str = Query(..., min_length=1),
    domain: Optional[str] = None,
    project: Optional[str] = None,
    semantic: bool = False,
    limit: int = Query(50, le=200)
):
    """Search knowledge entries"""
    try:
        filters = {
            'domain': domain,
            'project': project,
            'semantic': semantic,
            'limit': limit
        }
        results = brain.search_entries(q, user_id='faza', filters=filters)  # TODO: Get from auth
        return {'results': results, 'count': len(results), 'query': q}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== EMBEDDINGS ==========

@router.post("/entries/{entry_id}/embed")
async def generate_embedding(entry_id: str):
    """Generate vector embedding for knowledge entry"""
    try:
        result = brain.generate_embedding(entry_id)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== STATISTICS ==========

@router.get("/stats")
async def get_stats():
    """Get knowledge statistics"""
    try:
        stats = brain.get_stats(user_id='faza')  # TODO: Get from auth
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== SYNC ==========

@router.post("/sync/ankiw")
async def sync_anki():
    """Sync with AnkiWeb"""
    # TODO: Implement AnkiConnect sync
    return {'status': 'pending', 'message': 'AnkiWeb sync not implemented yet'}


@router.post("/sync/embeddings")
async def sync_embeddings():
    """Re-generate embeddings for all entries"""
    # TODO: Implement batch embedding generation
    return {'status': 'pending', 'message': 'Batch embedding sync not implemented yet'}
