# AAC System - Module 3: The Circle (Social CRM)

## Overview
Relationships → Health Logs → Couple Journal → Insights

## Components

### 1. Contact Management
- **Inner Circle Tracking:** Close relationships (family, mentors, best friends)
- **Contact Frequency:** Weekly, biweekly, monthly, quarterly check-ins
- **Birthday Reminders:** Important dates (birthday, anniversary, etc.)
- **Relationship Types:** Family, friend, colleague, mentor, other
- **Contact Channels:** Phone, email, Telegram, etc.

### 2. Health Logs (Gaby Protocol)
- **Symptom Types:**
  - Allergy - Allergic reactions, triggers
  - Reflux - Acid reflux episodes
  - Mood - Emotional state tracking
  - Energy - Energy levels throughout day
  - Pain - Any pain or discomfort
  - Sleep - Sleep quality issues

- **Tracked Fields:**
  - Severity (1-10 scale)
  - Triggers (food, stress, environment, etc.)
  - Location (where it happened)
  - Meal before (what was eaten)
  - Stress level (1-10)
  - Sleep quality (1-10)
  - Description (free text)
  - Remedy tried
  - Remedy effectiveness (1-10)

### 3. Couple Journal (Relationship Check-ins)
- **Daily/Weekly Check-ins:**
  - Faza mood (1-10)
  - Gaby mood (1-10)
  - Relationship vibe (1-10)
  - Topics discussed
  - Friction points
  - Wins
  - AI insights

- **Trend Analysis:**
  - Mood trends over time
  - Relationship health score
  - Conflict patterns
  - Positive moments tracking

### 4. Insights & Notifications
- **Contact Reminders:** "It's been 3 weeks since you talked to Sarah"
- **Health Alerts:** "Reflux episodes increased this week"
- **Relationship Warnings:** "Relationship vibe declining for 7 days"
- **Pattern Detection:** "Reflux triggered by spicy food 80% of the time"

## API Endpoints

```
POST /api/v1/circle/contacts
  - Add new contact
  - Set inner circle status

GET /api/v1/circle/contacts
  - List contacts (with filters)

GET /api/v1/circle/contacts/{id}
  - Get contact with history

PUT /api/v1/circle/contacts/{id}
  - Update contact info

POST /api/v1/circle/health-logs
  - Log health episode

GET /api/v1/circle/health-logs
  - Get health logs (with filters)

GET /api/v1/circle/health-logs/{id}
  - Get single health log

GET /api/v1/circle/health-logs/analysis
  - Get health analysis and triggers

POST /api/v1/circle/checkins
  - Create relationship check-in

GET /api/v1/circle/checkins
  - Get check-in history

GET /api/v1/circle/checkins/trends
  - Get mood and relationship trends

GET /api/v1/circle/reminders
  - Get pending reminders (contacts, health, etc.)
```

## Data Model

### Contact
```python
{
    "id": "cnt_xxxxxxxx",
    "name": "Sarah Johnson",
    "relationship": "friend",
    "inner_circle": true,
    "phone": "+1-555-1234",
    "email": "sarah@example.com",
    "telegram_handle": "@sarahj",
    "last_contact_date": "2026-02-15",
    "contact_frequency": "monthly",
    "next_scheduled_ping": "2026-03-15",
    "birthday": "1990-05-20",
    "important_dates": [
        {"date": "2026-05-20", "description": "Birthday - 36 years old"},
        {"date": "2026-08-15", "description": "Wedding Anniversary"}
    ],
    "notes": "Met at university, loves hiking"
}
```

### Health Log
```python
{
    "id": "hlg_xxxxxxxx",
    "timestamp": "2026-02-18T14:30:00Z",
    "owner": "gaby",
    "logged_by": "faza",
    "symptom_type": "reflux",
    "severity": 7,
    "triggers": ["spicy food", "late dinner"],
    "location": "home",
    "meal_before": "Indian curry",
    "stress_level": 6,
    "sleep_quality": 5,
    "description": "Burning sensation in chest after dinner",
    "remedy_tried": "Tums",
    "remedy_effectiveness": 4
}
```

### Relationship Check-in
```python
{
    "id": "rchk_xxxxxxxx",
    "timestamp": "2026-02-18T20:00:00Z",
    "owner": "shared",
    "faza_mood": 7,
    "gaby_mood": 6,
    "relationship_vibe": 8,
    "topics_discussed": ["work", "weekend plans", "health"],
    "friction_points": null,
    "wins": "Had a nice dinner together",
    "sentiment_score": 0.75,
    "ai_insights": "Relationship health is stable. Both moods slightly above average."
}
```

## Implementation Plan

### Week 1: Foundation
- [x] Database schema (health_logs, contacts, relationship_checkins)
- [ ] CircleModule class (CRUD operations)
- [ ] Contact management
- [ ] Health logging

### Week 2: Health Analysis
- [ ] Trigger pattern detection
- [ ] Health correlation analysis
- [ ] Trend visualization
- [ ] Alert system

### Week 3: Relationship Tracking
- [ ] Couple journal (check-ins)
- [ ] Mood trend analysis
- [ ] Sentiment analysis
- [ ] Conflict detection

### Week 4: Reminders & Insights
- [ ] Contact reminders system
- [ ] Health alerts
- [ ] Relationship insights
- [ ] Notification system

## File Structure

```
modules/circle/
├── __init__.py
├── models.py          # Dataclass models
├── service.py         # Business logic
├── api.py            # FastAPI routes
├── health.py          # Health analysis logic
├── insights.py        # Insights and patterns
└── reminders.py       # Reminder system
```

## Dependencies

- **Schedule:** For reminder scheduling
- **Dateutil:** For date calculations
- **Pandas:** For trend analysis and correlation

## Quick Start

```bash
# Log a health episode
curl -X POST http://localhost:8000/api/v1/circle/health-logs \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "gaby",
    "symptom_type": "reflux",
    "severity": 7,
    "triggers": ["spicy food"],
    "description": "Burning in chest after dinner"
  }'

# Add a contact
curl -X POST http://localhost:8000/api/v1/circle/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "relationship": "friend",
    "inner_circle": true,
    "contact_frequency": "monthly",
    "phone": "+1-555-1234"
  }'

# Create relationship check-in
curl -X POST http://localhost:8000/api/v1/circle/checkins \
  -H "Content-Type: application/json" \
  -d '{
    "faza_mood": 7,
    "gaby_mood": 8,
    "relationship_vibe": 9,
    "topics_discussed": ["work", "plans"],
    "wins": "Great dinner tonight"
  }'
```

## Gaby Protocol (Health Tracking)

The Circle module is specifically designed for Gaby's health tracking:

1. **Allergy Tracking:**
   - Identify allergens (nuts, shellfish, pollen, etc.)
   - Track reaction severity
   - Log exposure triggers

2. **Acid Reflux Management:**
   - Track reflux episodes
   - Identify food triggers
   - Monitor effectiveness of remedies
   - Correlate with sleep quality and stress

3. **Mood & Energy:**
   - Daily mood tracking
   - Energy levels throughout day
   - Identify patterns and triggers

4. **Insights:**
   - "Reflux occurs 3x more after spicy food"
   - "Allergy reactions peak during spring"
   - "Mood declines when sleep quality < 5"
