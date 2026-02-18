"""
Models for The Vessel module (using dataclasses - no pydantic dependency)
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class BlueprintLogCreate:
    """Create a Blueprint protocol log"""
    owner: str
    date: str
    supplements_taken: bool = False
    super_veggie_eaten: bool = False
    nutty_pudding_eaten: bool = False
    exercise_done: bool = False
    supplement_list: Optional[List[Dict]] = field(default_factory=list)
    meals_logged: Optional[List[Dict]] = field(default_factory=list)
    water_intake_ml: Optional[int] = None


@dataclass
class WorkoutCreate:
    """Create a workout log"""
    owner: str
    workout_type: str  # hyperpump, cardio, recovery, mobility
    location: Optional[str] = None
    duration_minutes: int = 0
    total_volume_kg: int = 0
    avg_rpe: Optional[float] = None
    prs_achieved: Optional[List[Dict]] = field(default_factory=list)
    exercises: Optional[List[Dict]] = field(default_factory=list)


@dataclass
class BiometricCreate:
    """Create a biometric entry"""
    owner: str
    date: str
    sleep_score: Optional[int] = None
    sleep_hours: Optional[float] = None
    deep_sleep_pct: Optional[float] = None
    hrv: Optional[int] = None
    resting_hr: Optional[int] = None
    recovery_score: Optional[int] = None
    weight_kg: Optional[float] = None
    body_fat_pct: Optional[float] = None
    device_source: Optional[str] = None


@dataclass
class SobrietyTrackerCreate:
    """Create a sobriety tracker"""
    owner: str
    habit_type: str  # alcohol, nicotine, caffeine, social_media, gaming, other
    start_date: str
    why_i_started: Optional[str] = None


@dataclass
class RelapseLog:
    """Log a relapse"""
    relapse_date: str
    reason: Optional[str] = None
    triggers: Optional[List[str]] = None
    cost: Optional[float] = None


@dataclass
class AnalyticsFilters:
    """Filters for analytics queries"""
    owner: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include_blueprint: bool = True
    include_workouts: bool = True
    include_biometrics: bool = True
