"""
API routes for The Circle module (Social CRM)
FastAPI endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from .service import CircleModule


router = APIRouter(prefix="/api/v1/circle", tags=["circle"])
circle = CircleModule()


# ========== CONTACT ENDPOINTS ==========

@router.post("/contacts")
async def create_contact(contact_data: dict):
    """Create a new contact"""
    try:
        result = circle.create_contact(contact_data, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contacts")
async def list_contacts(
    inner_circle_only: bool = False,
    relationship: Optional[str] = None
):
    """List contacts"""
    try:
        contacts = circle.get_contacts(
            user_id='faza',  # TODO: Get from auth
            inner_circle_only=inner_circle_only,
            relationship=relationship
        )
        return {'contacts': contacts, 'count': len(contacts)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: str):
    """Get a single contact"""
    try:
        contact = circle.get_contact(contact_id, user_id='faza')  # TODO: Get from auth
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: str, update_data: dict):
    """Update a contact"""
    try:
        result = circle.update_contact(contact_id, update_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/contacts/{contact_id}/contact")
async def record_contact(contact_id: str):
    """Record that you contacted this person"""
    try:
        result = circle.record_contact(contact_id, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== HEALTH LOG ENDPOINTS ==========

@router.post("/health-logs")
async def create_health_log(log_data: dict):
    """Create a health log entry"""
    try:
        result = circle.create_health_log(log_data, logged_by='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health-logs")
async def list_health_logs(
    owner: Optional[str] = None,
    symptom_type: Optional[str] = None,
    days: int = Query(30, le=365)
):
    """List health logs"""
    try:
        logs = circle.get_health_logs(
            user_id='faza',  # TODO: Get from auth
            owner=owner,
            symptom_type=symptom_type,
            days=days
        )
        return {'logs': logs, 'count': len(logs)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health-logs/{log_id}")
async def get_health_log(log_id: str):
    """Get a single health log"""
    try:
        log = circle.get_health_log(log_id, user_id='faza')  # TODO: Get from auth
        if not log:
            raise HTTPException(status_code=404, detail="Health log not found")
        return log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health-logs/analysis")
async def analyze_health(
    owner: str,
    symptom_type: str,
    days: int = Query(30, le=365)
):
    """Analyze health logs for patterns"""
    try:
        analysis = circle.analyze_health(owner, symptom_type, days)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== CHECK-IN ENDPOINTS ==========

@router.post("/checkins")
async def create_checkin(checkin_data: dict):
    """Create a relationship check-in"""
    try:
        result = circle.create_checkin(checkin_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checkins")
async def list_checkins(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_vibe: Optional[int] = None,
    limit: int = Query(50, le=200)
):
    """List relationship check-ins"""
    try:
        checkins = circle.get_checkins(
            start_date=start_date,
            end_date=end_date,
            min_vibe=min_vibe,
            limit=limit
        )
        return {'checkins': checkins, 'count': len(checkins)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checkins/trends")
async def get_checkin_trends(days: int = Query(30, le=90)):
    """Get mood and relationship trends"""
    try:
        trends = circle.get_checkin_trends(days=days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== REMINDERS ==========

@router.get("/reminders")
async def get_reminders():
    """Get pending reminders"""
    try:
        reminders = circle.get_reminders(user_id='faza')  # TODO: Get from auth
        return reminders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== STATISTICS ==========

@router.get("/stats")
async def get_stats():
    """Get Circle module statistics"""
    try:
        stats = circle.get_stats(user_id='faza')  # TODO: Get from auth
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
