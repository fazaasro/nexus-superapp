"""
Models for The Circle module (using dataclasses - no pydantic dependency)
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class ContactCreate:
    """Create a new contact"""
    name: str
    relationship: str  # family, friend, colleague, mentor, other
    inner_circle: bool = False
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_handle: Optional[str] = None
    contact_frequency: Optional[str] = None  # weekly, biweekly, monthly, quarterly
    birthday: Optional[str] = None
    important_dates: Optional[List[Dict]] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class ContactUpdate:
    """Update a contact"""
    name: Optional[str] = None
    relationship: Optional[str] = None
    inner_circle: Optional[bool] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_handle: Optional[str] = None
    last_contact_date: Optional[str] = None
    contact_frequency: Optional[str] = None
    next_scheduled_ping: Optional[str] = None
    important_dates: Optional[List[Dict]] = None
    notes: Optional[str] = None


@dataclass
class HealthLogCreate:
    """Create a health log entry"""
    owner: str  # faza or gaby
    symptom_type: str  # allergy, reflux, mood, energy, pain, sleep
    severity: int  # 1-10
    triggers: Optional[List[str]] = field(default_factory=list)
    location: Optional[str] = None
    meal_before: Optional[str] = None
    stress_level: Optional[int] = None  # 1-10
    sleep_quality: Optional[int] = None  # 1-10
    description: Optional[str] = None
    remedy_tried: Optional[str] = None
    remedy_effectiveness: Optional[int] = None  # 1-10


@dataclass
class CheckinCreate:
    """Create a relationship check-in"""
    faza_mood: int  # 1-10
    gaby_mood: int  # 1-10
    relationship_vibe: int  # 1-10
    topics_discussed: Optional[List[str]] = field(default_factory=list)
    friction_points: Optional[str] = None
    wins: Optional[str] = None


@dataclass
class CheckinFilters:
    """Filters for check-in queries"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    min_vibe: Optional[int] = None
    has_friction: Optional[bool] = None


@dataclass
class HealthAnalysis:
    """Health analysis result"""
    symptom_type: str
    episode_count: int
    avg_severity: float
    common_triggers: List[Dict[str, int]]  # trigger -> count
    severity_trend: str  # improving, stable, worsening
    insights: List[str]
