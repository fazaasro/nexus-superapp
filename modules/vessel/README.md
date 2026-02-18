# AAC System - Module 4: The Vessel (Health Tracking)

## Overview
Blueprint Protocol → Empire Fit → Biometrics → Trends & Analytics

## Components

### 1. Blueprint Protocol (Daily Compliance)
- **Daily Checklist:**
  - Supplements taken (Blueprint protocol)
  - Super veggie eaten
  - Nutty pudding eaten
  - Exercise done
  - Water intake

- **Tracking:**
  - Supplement list (what was taken)
  - Meals logged (what was eaten)
  - Compliance score (0-100%)

### 2. Empire Fit (Workouts)
- **Workout Types:**
  - Hyperpump - Hypertrophy-focused lifting
  - Cardio - Cardiovascular training
  - Recovery - Active recovery, stretching
  - Mobility - Flexibility work

- **Metrics Tracked:**
  - Duration (minutes)
  - Total volume (kg lifted)
  - Average RPE (Rate of Perceived Exertion)
  - PRs achieved (personal records)
  - Exercises performed

### 3. Biometrics (Health Metrics)
- **Sleep:**
  - Sleep score (1-100)
  - Sleep hours
  - Deep sleep percentage
  - Recovery score

- **Heart Health:**
  - HRV (Heart Rate Variability)
  - Resting heart rate

- **Body Composition:**
  - Weight (kg)
  - Body fat percentage

- **Source Devices:**
  - Whoop strap
  - Oura ring
  - Apple Watch
  - Garmin
  - Manual entry

### 4. Sobriety Tracker
- **Habits Tracked:**
  - Alcohol
  - Nicotine
  - Caffeine
  - Social media
  - Gaming
  - Other

- **Metrics:**
  - Start date
  - Last relapse date
  - Current streak (days)
  - Longest streak (days)
  - Savings calculated
  - Relapse log

## API Endpoints

```
POST /api/v1/vessel/blueprint
  - Log daily Blueprint protocol compliance

GET /api/v1/vessel/blueprint
  - Get Blueprint logs (with filters)

GET /api/v1/vessel/blueprint/{date}
  - Get specific day's Blueprint log

POST /api/v1/vessel/workouts
  - Log a workout

GET /api/v1/vessel/workouts
  - Get workout history

GET /api/v1/vessel/workouts/stats
  - Get workout statistics

POST /api/v1/vessel/biometrics
  - Log biometric data

GET /api/v1/vessel/biometrics
  - Get biometric history

GET /api/v1/vessel/biometrics/trends
  - Get biometric trends

POST /api/v1/vessel/sobriety
  - Start sobriety tracker

PUT /api/v1/vessel/sobriety/{id}/relapse
  - Log a relapse

GET /api/v1/vessel/sobriety/{id}
  - Get sobriety tracker status

GET /api/v1/vessel/analytics
  - Get overall health analytics
```

## Data Model

### Blueprint Log
```python
{
    "id": "bpl_xxxxxxxx",
    "timestamp": "2026-02-18T23:59:59Z",
    "owner": "faza",
    "date": "2026-02-18",
    "supplements_taken": true,
    "super_veggie_eaten": true,
    "nutty_pudding_eaten": true,
    "exercise_done": true,
    "supplement_list": [
        {"name": "Vitamin D3", "dosage": "5000 IU"},
        {"name": "Omega-3", "dosage": "2000 mg"},
        {"name": "Magnesium", "dosage": "400 mg"}
    ],
    "meals_logged": [
        {"meal": "breakfast", "description": "Oatmeal with berries"},
        {"meal": "lunch", "description": "Grilled chicken salad"}
    ],
    "water_intake_ml": 2500,
    "compliance_score": 100
}
```

### Workout Log
```python
{
    "id": "wrk_xxxxxxxx",
    "timestamp": "2026-02-18T10:30:00Z",
    "owner": "faza",
    "workout_type": "hyperpump",
    "location": "gym",
    "duration_minutes": 75,
    "total_volume_kg": 12500,
    "avg_rpe": 7.5,
    "prs_achieved": [
        {"exercise": "Bench Press", "weight": "100 kg", "reps": 5}
    ],
    "exercises": [
        {"name": "Bench Press", "sets": 4, "reps": "8-10", "weight": "90 kg"},
        {"name": "Squat", "sets": 4, "reps": "8-10", "weight": "120 kg"}
    ]
}
```

### Biometric Entry
```python
{
    "id": "bio_xxxxxxxx",
    "timestamp": "2026-02-18T08:00:00Z",
    "owner": "faza",
    "date": "2026-02-18",
    "sleep_score": 85,
    "sleep_hours": 7.5,
    "deep_sleep_pct": 22.5,
    "hrv": 55,
    "resting_hr": 62,
    "recovery_score": 78,
    "weight_kg": 82.5,
    "body_fat_pct": 18.2,
    "device_source": "Whoop"
}
```

### Sobriety Tracker
```python
{
    "id": "sob_xxxxxxxx",
    "owner": "faza",
    "habit_type": "alcohol",
    "start_date": "2025-01-01",
    "last_relapse": null,
    "current_streak_days": 413,
    "longest_streak_days": 413,
    "relapse_log": [],
    "why_i_started": "Wanted to improve health and save money",
    "savings_calculated": 1645.50
}
```

## Implementation Plan

### Week 1: Foundation
- [x] Database schema (blueprint_logs, workouts, biometrics, sobriety_tracker)
- [ ] VesselModule class (CRUD operations)
- [ ] Blueprint protocol tracking
- [ ] Workout logging

### Week 2: Biometrics Integration
- [ ] Biometric data logging
- [ ] Trend analysis
- [ ] Device integration (Whoop, Oura, etc.)

### Week 3: Sobriety Tracking
- [ ] Sobriety tracker
- [ ] Relapse logging
- [ ] Streak calculation
- [ ] Savings calculation

### Week 4: Analytics & Insights
- [ ] Compliance tracking
- [ ] Performance trends
- [ ] Health correlations
- [ ] Goal tracking

## File Structure

```
modules/vessel/
├── __init__.py
├── models.py          # Dataclass models
├── service.py         # Business logic
├── api.py            # FastAPI routes
├── blueprint.py       # Blueprint protocol logic
├── workouts.py        # Workout tracking logic
├── biometrics.py      # Biometric analysis
└── sobriety.py        # Sobriety tracker
```

## Dependencies

- **Pandas:** For trend analysis and data manipulation
- **Numpy:** For statistical calculations
- **Dateutil:** For date calculations

## Quick Start

```bash
# Log Blueprint protocol
curl -X POST http://localhost:8000/api/v1/vessel/blueprint \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "faza",
    "date": "2026-02-18",
    "supplements_taken": true,
    "super_veggie_eaten": true,
    "nutty_pudding_eaten": true,
    "exercise_done": true,
    "water_intake_ml": 2500
  }'

# Log workout
curl -X POST http://localhost:8000/api/v1/vessel/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "faza",
    "workout_type": "hyperpump",
    "location": "gym",
    "duration_minutes": 75,
    "total_volume_kg": 12500,
    "avg_rpe": 7.5
  }'

# Log biometrics
curl -X POST http://localhost:8000/api/v1/vessel/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "faza",
    "date": "2026-02-18",
    "sleep_score": 85,
    "sleep_hours": 7.5,
    "hrv": 55,
    "resting_hr": 62,
    "weight_kg": 82.5
  }'
```

## Blueprint Protocol Details

The Blueprint protocol is Faza's daily health routine:

1. **Supplements:** Morning stack (Vitamin D3, Omega-3, Magnesium, etc.)
2. **Super Veggie:** Daily serving of nutrient-dense vegetables
3. **Nutty Pudding:** Healthy fat/protein snack
4. **Exercise:** Minimum 30 minutes of movement
5. **Water:** Minimum 2.5 liters of water

**Compliance Score:** Calculated as percentage of daily goals met:
- Supplements: 20 points
- Super veggie: 20 points
- Nutty pudding: 20 points
- Exercise: 20 points
- Water: 20 points

## Empire Fit Details

Empire Fit is the workout program with four types:

1. **Hyperpump:** Hypertrophy-focused lifting (3x/week)
   - Focus: Muscle growth
   - Reps: 8-12 range
   - Rest: 90-120s between sets

2. **Cardio:** Cardiovascular training (2x/week)
   - Focus: Heart health, fat loss
   - Types: Running, cycling, rowing, HIIT

3. **Recovery:** Active recovery (1x/week)
   - Focus: Rest, mobility
   - Types: Walking, yoga, stretching

4. **Mobility:** Flexibility work (daily)
   - Focus: Joint health, range of motion
   - Duration: 10-15 minutes

## Analytics Features

- **Compliance Trends:** Blueprint protocol compliance over time
- **Performance Progress:** Workout volume, PRs, RPE trends
- **Health Correlations:** Biometric trends vs. performance
- **Sobriety Milestones:** Streak achievements, savings calculated
- **Goal Tracking:** Set and track health and fitness goals
