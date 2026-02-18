"""
API routes for The Vessel module (Health Tracking)
FastAPI endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from .service import VesselModule


router = APIRouter(prefix="/api/v1/vessel", tags=["vessel"])
vessel = VesselModule()


# ========== BLUEPRINT PROTOCOL ENDPOINTS ==========

@router.post("/blueprint")
async def log_blueprint(blueprint_data: dict):
    """Log Blueprint protocol compliance"""
    try:
        result = vessel.log_blueprint(blueprint_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/blueprint")
async def list_blueprint_logs(
    owner: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(30, le=100)
):
    """List Blueprint logs"""
    try:
        logs = vessel.get_blueprint_logs(
            user_id='faza',  # TODO: Get from auth
            owner=owner,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return {'logs': logs, 'count': len(logs)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/blueprint/{log_date}")
async def get_blueprint_log(log_date: str, owner: str):
    """Get Blueprint log for a specific date"""
    try:
        log = vessel.get_blueprint_log(log_date, owner, user_id='faza')  # TODO: Get from auth
        if not log:
            raise HTTPException(status_code=404, detail="Blueprint log not found")
        return log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== WORKOUT ENDPOINTS ==========

@router.post("/workouts")
async def log_workout(workout_data: dict):
    """Log a workout"""
    try:
        result = vessel.log_workout(workout_data, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/workouts")
async def list_workouts(
    owner: Optional[str] = None,
    workout_type: Optional[str] = None,
    days: int = Query(30, le=365)
):
    """List workouts"""
    try:
        workouts = vessel.get_workouts(
            user_id='faza',  # TODO: Get from auth
            owner=owner,
            workout_type=workout_type,
            days=days
        )
        return {'workouts': workouts, 'count': len(workouts)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/workouts/stats")
async def get_workout_stats(owner: str, days: int = Query(30, le=365)):
    """Get workout statistics"""
    try:
        stats = vessel.get_workout_stats(owner, days=days)
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== BIOMETRICS ENDPOINTS ==========

@router.post("/biometrics")
async def log_biometrics(biometric_data: dict):
    """Log biometric data"""
    try:
        result = vessel.log_biometrics(biometric_data, user_id='faza')  # TODO: Get from auth
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/biometrics")
async def list_biometrics(
    owner: Optional[str] = None,
    days: int = Query(30, le=365)
):
    """List biometric history"""
    try:
        biometrics = vessel.get_biometrics(
            user_id='faza',  # TODO: Get from auth
            owner=owner,
            days=days
        )
        return {'biometrics': biometrics, 'count': len(biometrics)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/biometrics/trends")
async def get_biometric_trends(owner: str, days: int = Query(30, le=365)):
    """Get biometric trends"""
    try:
        trends = vessel.get_biometric_trends(owner, days=days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== SOBRIETY TRACKER ENDPOINTS ==========

@router.post("/sobriety")
async def start_sobriety_tracker(tracker_data: dict):
    """Start sobriety tracker"""
    try:
        result = vessel.start_sobriety_tracker(tracker_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sobriety/{tracker_id}")
async def get_sobriety_tracker(tracker_id: str):
    """Get sobriety tracker status"""
    try:
        tracker = vessel.get_sobriety_tracker(tracker_id, user_id='faza')  # TODO: Get from auth
        if not tracker:
            raise HTTPException(status_code=404, detail="Sobriety tracker not found")
        return tracker
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/sobriety/{tracker_id}/relapse")
async def log_relapse(tracker_id: str, relapse_data: dict):
    """Log a relapse"""
    try:
        result = vessel.log_relapse(tracker_id, relapse_data, user_id='faza')  # TODO: Get from auth
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== ANALYTICS ENDPOINTS ==========

@router.get("/analytics")
async def get_analytics(owner: str, days: int = Query(30, le=90)):
    """Get overall health analytics"""
    try:
        analytics = vessel.get_analytics(owner, days=days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== STATISTICS ==========

@router.get("/stats")
async def get_stats(owner: Optional[str] = None):
    """Get Vessel module statistics"""
    try:
        stats = vessel.get_stats(user_id='faza', owner=owner)  # TODO: Get from auth
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
