"""
API routes for The Brain module (Knowledge Management)
FastAPI endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from datetime import datetime

from .service import BrainModule
from core.auth import get_current_user_cloudflare


router = APIRouter(prefix="/api/v1/brain", tags=["brain"])
brain = BrainModule()
get_current_user = get_current_user_cloudflare


# ========== KNOWLEDGE ENTRY ENDPOINTS ==========

@router.post("/entries")
async def create_entry(entry_data: dict, user: dict = Depends(get_current_user)):
    """Create a new knowledge entry"""
    try:
        result = brain.create_entry(entry_data, user_id=user['user_id'])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/entries")
async def list_entries(
    domain: Optional[str] = None,
    project: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = Query(50, le=200),
    user: dict = Depends(get_current_user)
):
    """List knowledge entries"""
    try:
        entries = brain.get_entries(
            user_id=user['user_id'],
            domain=domain,
            project=project,
            content_type=content_type,
            limit=limit
        )
        return {'entries': entries, 'count': len(entries)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/entries/{entry_id}")
async def get_entry(entry_id: str, user: dict = Depends(get_current_user)):
    """Get a single knowledge entry"""
    try:
        entry = brain.get_entry(entry_id, user_id=user['user_id'])
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/entries/{entry_id}")
async def update_entry(entry_id: str, update_data: dict, user: dict = Depends(get_current_user)):
    """Update a knowledge entry"""
    try:
        result = brain.update_entry(entry_id, update_data, user_id=user['user_id'])
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str, user: dict = Depends(get_current_user)):
    """Delete a knowledge entry"""
    try:
        result = brain.delete_entry(entry_id, user_id=user['user_id'])
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== ANKI INTEGRATION ==========

@router.post("/entries/{entry_id}/anki")
async def create_anki_card(entry_id: str, user: dict = Depends(get_current_user)):
    """Create Anki card from knowledge entry"""
    try:
        result = brain.create_anki_card(entry_id, user_id=user['user_id'])
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== WEB CLIPPING ==========

@router.post("/clip")
async def create_web_clip(url_data: dict, user: dict = Depends(get_current_user)):
    """Clip a web page as knowledge entry"""
    try:
        url = url_data.get('url')
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        result = brain.create_web_clip(url, user_id=user['user_id'], metadata=url_data)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== WORKTREE MANAGEMENT ==========

@router.post("/worktrees")
async def create_worktree(worktree_data: dict, user: dict = Depends(get_current_user)):
    """Create a git worktree entry"""
    try:
        result = brain.create_worktree(worktree_data, user_id=user['user_id'])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/worktrees")
async def list_worktrees(status: Optional[str] = None, user: dict = Depends(get_current_user)):
    """List worktrees"""
    try:
        worktrees = brain.get_worktrees(user_id=user['user_id'], status=status)
        return {'worktrees': worktrees, 'count': len(worktrees)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/worktrees/{worktree_id}/access")
async def update_worktree_access(worktree_id: str, user: dict = Depends(get_current_user)):
    """Update last access time for worktree"""
    try:
        result = brain.update_worktree_access(worktree_id, user_id=user['user_id'])
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
    limit: int = Query(50, le=200),
    user: dict = Depends(get_current_user)
):
    """Search knowledge entries"""
    try:
        filters = {
            'domain': domain,
            'project': project,
            'semantic': semantic,
            'limit': limit
        }
        results = brain.search_entries(q, user_id=user['user_id'], filters=filters)
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
async def get_stats(user: dict = Depends(get_current_user)):
    """Get knowledge statistics"""
    try:
        stats = brain.get_stats(user_id=user['user_id'])
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== SYNC ==========

@router.post("/sync/anki")
async def sync_anki(user: dict = Depends(get_current_user)):
    """Sync with AnkiWeb"""
    try:
        # Trigger AnkiConnect to sync with AnkiWeb
        # This requires Anki to be running with AnkiConnect add-on
        result = brain._trigger_anki_sync()
        return {'status': 'completed', 'message': 'AnkiWeb sync triggered', 'result': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sync/embeddings")
async def sync_embeddings(user: dict = Depends(get_current_user)):
    """Re-generate embeddings for all entries"""
    try:
        # Get all entries for user
        entries = brain.get_entries(user_id=user['user_id'], include_shared=True, limit=1000)

        # Generate embeddings for each entry
        success_count = 0
        failed_count = 0

        for entry in entries:
            try:
                brain.generate_embedding(entry['id'])
                success_count += 1
            except Exception as e:
                logger.error(f"Error generating embedding for {entry['id']}: {e}")
                failed_count += 1

        return {
            'status': 'completed',
            'success_count': success_count,
            'failed_count': failed_count,
            'total': len(entries)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
