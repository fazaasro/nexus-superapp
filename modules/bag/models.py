"""
Models for The Bag module (using dataclasses - no pydantic dependency)
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class TransactionCreate:
    """Create a new transaction"""
    merchant: str
    amount: float
    currency: str = "EUR"
    category: Optional[str] = "lifestyle"
    impact_score: int = 3
    owner: Optional[str] = None
    split_type: Optional[str] = "solo"
    faza_portion: Optional[float] = None
    gaby_portion: Optional[float] = None
    is_business: Optional[bool] = False
    client: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)
    location: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    raw_text: Optional[str] = None
    source_image: Optional[str] = None


@dataclass
class SplitUpdate:
    """Update split for a transaction"""
    split_type: str
    faza_portion: Optional[float] = None
    gaby_portion: Optional[float] = None


@dataclass
class SubscriptionCreate:
    """Create a subscription"""
    merchant: str
    amount: float
    frequency: str = "monthly"
    next_payment: Optional[str] = None
    category: Optional[str] = "lifestyle"
    is_essential: Optional[bool] = False
    cancellation_url: Optional[str] = None


@dataclass
class BudgetCreate:
    """Create a budget"""
    name: str
    amount: float
    category: str = "all"
    period: str = "monthly"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
