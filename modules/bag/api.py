"""
FastAPI routes for The Bag module (without pydantic)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional

from core.database import get_user_from_email
from core.auth import get_current_user_cloudflare
from modules.bag.service import BagModule

router = APIRouter()
bag = BagModule()
get_current_user = get_current_user_cloudflare

router = APIRouter()
bag = BagModule()


@router.get("/health")
async def bag_health():
    """Health check for bag module"""
    return {"module": "bag", "status": "ok"}


# ========== TRANSACTIONS ==========

@router.post("/transactions")
async def create_transaction(data: dict, user: dict = Depends(get_current_user)):
    """Create a new transaction"""
    result = bag.create_transaction(data, user['user_id'])
    return result


@router.get("/transactions")
async def get_transactions(
    category: Optional[str] = None,
    limit: int = 50,
    include_shared: bool = True,
    user: dict = Depends(get_current_user)
):
    """Get transactions for current user"""
    transactions = bag.get_transactions(
        user['user_id'], 
        include_shared=include_shared,
        category=category,
        limit=limit
    )
    return transactions


@router.post("/transactions/{txn_id}/split")
async def update_split(
    txn_id: str,
    data: dict,
    user: dict = Depends(get_current_user)
):
    """Update split for a transaction"""
    result = bag.update_split(
        txn_id, 
        data.get('split_type', 'solo'), 
        user['user_id'],
        data.get('faza_portion'),
        data.get('gaby_portion')
    )
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    return result


# ========== RECEIPTS ==========

@router.post("/receipts/upload")
async def upload_receipt(
    file: UploadFile = File(...),
    notes: Optional[str] = None,
    user: dict = Depends(get_current_user)
):
    """Upload a receipt image for OCR processing"""
    import shutil
    from pathlib import Path
    
    upload_dir = Path("/tmp/receipts")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / f"{user['user_id']}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = bag.process_receipt(str(file_path), user['user_id'])
    
    return {
        "status": "uploaded",
        "file_path": str(file_path),
        "processing_result": result
    }


# ========== RUNWAY ==========

@router.get("/runway")
async def get_runway(
    current_balance: Optional[float] = None,
    user: dict = Depends(get_current_user)
):
    """Calculate days of survival remaining"""
    result = bag.calculate_runway(user['user_id'], current_balance)
    
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    
    return result


# ========== SUBSCRIPTIONS ==========

@router.get("/subscriptions/detect")
async def detect_subscriptions(user: dict = Depends(get_current_user)):
    """Detect potential subscriptions from transaction history"""
    patterns = bag.detect_subscriptions(user['user_id'])
    return {"patterns": patterns}


@router.post("/subscriptions")
async def create_subscription(data: dict, user: dict = Depends(get_current_user)):
    """Add a subscription to tracking"""
    result = bag.add_subscription(data, user['user_id'])
    return result


# ========== BUDGETS ==========

@router.post("/budgets")
async def create_budget(data: dict, user: dict = Depends(get_current_user)):
    """Create a budget"""
    result = bag.create_budget(data, user['user_id'])
    return result


@router.get("/budgets/{budget_id}/status")
async def get_budget_status(budget_id: str, user: dict = Depends(get_current_user)):
    """Get budget status"""
    result = bag.get_budget_status(budget_id)
    
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    
    return result
