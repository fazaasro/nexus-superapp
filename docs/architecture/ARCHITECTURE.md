# AAC System Architecture v1.0

*Fundamental architecture for The Bag, The Brain, The Circle, and The Vessel*

**Date:** 2026-02-08  
**Status:** Design Phase  
**Core Stack:** SQLite + Qdrant + n8n + FastAPI

---

## 1. Core Principles

### 1.1 Modular Design
- Each module (Bag, Brain, Circle, Vessel) is **independent**
- Modules communicate via **Event Bus** (n8n webhooks)
- Shared utilities in `core/`
- No circular dependencies

### 1.2 Multi-Tenant Data Model
```
User Contexts:
├── faza (private)
├── gaby (private)
└── shared (couple/family)
```

Every table has `owner` column: `faza` | `gaby` | `shared`

### 1.3 Data Flow
```
Input (WhatsApp/Telegram)
    ↓
Ingestion Service (n8n)
    ↓
[Classifier/Processor]
    ↓
SQLite (structured data) + Qdrant (embeddings)
    ↓
API Layer (FastAPI)
    ↓
Dashboard/Notifications
```

---

## 2. Database Architecture (SQLite)

### 2.1 Schema Design

```sql
-- Core: Users
CREATE TABLE users (
    id TEXT PRIMARY KEY,           -- 'faza', 'gaby', 'shared'
    email TEXT UNIQUE,
    name TEXT,
    timezone TEXT DEFAULT 'Europe/Berlin',
    preferences JSON               -- module-specific settings
);

-- Core: Audit Log (everything traces here)
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT,
    module TEXT,                   -- 'bag', 'brain', 'circle', 'vessel'
    action TEXT,                   -- 'create', 'update', 'delete', 'query'
    entity_type TEXT,              -- 'transaction', 'note', 'symptom', etc.
    entity_id TEXT,
    metadata JSON,                 -- additional context
    ip_address TEXT
);

-- ==================== MODULE 1: THE BAG ====================

CREATE TABLE transactions (
    id TEXT PRIMARY KEY,           -- UUID
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,                    -- 'faza', 'gaby', 'shared'
    created_by TEXT,               -- who logged it
    
    -- Raw input
    raw_text TEXT,                 -- OCR output or manual entry
    source_image TEXT,             -- path to receipt image
    
    -- Classified data
    merchant TEXT,
    amount DECIMAL(10,2),
    currency TEXT DEFAULT 'EUR',
    category TEXT,                 -- 'survival', 'health', 'lifestyle', 'trash', 'income'
    impact_score INTEGER,          -- 1-5 (AI calculated)
    
    -- Split logic (for shared expenses)
    split_type TEXT,               -- 'solo', 'split_equal', 'split_custom'
    faza_portion DECIMAL(3,2) DEFAULT 1.0,  -- 0.0 to 1.0
    gaby_portion DECIMAL(3,2) DEFAULT 0.0,
    
    -- Business mode
    is_business BOOLEAN DEFAULT 0,
    client TEXT,                   -- for consulting expenses
    
    -- Tags
    tags JSON,                     -- ['bali2026', 'recurring', 'subscription']
    
    -- Metadata
    location TEXT,                 -- GPS or manual
    payment_method TEXT,
    notes TEXT
);

CREATE TABLE budgets (
    id TEXT PRIMARY KEY,
    owner TEXT,
    name TEXT,                     -- 'Monthly Survival', 'Bali 2026'
    category TEXT,                 -- or 'all'
    amount DECIMAL(10,2),
    period TEXT,                   -- 'weekly', 'monthly', 'yearly'
    start_date DATE,
    end_date DATE                  -- null = ongoing
);

CREATE TABLE subscriptions (
    id TEXT PRIMARY KEY,
    owner TEXT,
    merchant TEXT,
    amount DECIMAL(10,2),
    frequency TEXT,                -- 'weekly', 'monthly', 'yearly'
    next_payment DATE,
    category TEXT,
    is_essential BOOLEAN,          -- for ghost-hunter alerts
    cancellation_url TEXT,
    status TEXT DEFAULT 'active'   -- 'active', 'cancelled', 'paused'
);

-- ==================== MODULE 2: THE BRAIN ====================

CREATE TABLE knowledge_entries (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,
    created_by TEXT,
    
    -- Content
    title TEXT,
    content TEXT,                  -- markdown
    content_type TEXT,             -- 'note', 'voice_transcript', 'web_clip', 'code'
    
    -- Source
    source_url TEXT,
    source_file TEXT,
    
    -- Classification
    domain TEXT,                   -- 'tech', 'dnd', 'masters', 'life'
    project TEXT,                  -- 'zscaler-bypass', 'campaign-1'
    tags JSON,
    
    -- For SRS/Anki
    is_srs_eligible BOOLEAN DEFAULT 0,
    srs_card_id TEXT,              -- link to anki if exported
    
    -- Qdrant sync
    qdrant_id TEXT,                -- vector DB reference
    embedding_synced BOOLEAN DEFAULT 0
);

CREATE TABLE worktrees (
    id TEXT PRIMARY KEY,
    owner TEXT,
    repo_name TEXT,
    branch_name TEXT,
    worktree_path TEXT,
    status TEXT,                   -- 'active', 'archived', 'merged'
    last_accessed DATETIME,
    context_notes TEXT             -- what was I working on?
);

-- ==================== MODULE 3: THE CIRCLE ====================

CREATE TABLE health_logs (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,                    -- who's logging (usually gaby for her protocol)
    logged_by TEXT,                -- who actually recorded it
    
    -- Symptoms
    symptom_type TEXT,             -- 'allergy', 'reflux', 'mood', 'energy'
    severity INTEGER,              -- 1-10
    triggers JSON,                 -- ['dairy', 'stress', 'spicy_food']
    
    -- Context
    location TEXT,
    meal_before TEXT,
    stress_level INTEGER,          -- 1-10
    sleep_quality INTEGER,         -- 1-10
    
    -- Notes
    description TEXT,
    remedy_tried TEXT,
    remedy_effectiveness INTEGER   -- 1-10
);

CREATE TABLE contacts (
    id TEXT PRIMARY KEY,
    owner TEXT,                    -- who owns this contact
    name TEXT,
    relationship TEXT,             -- 'family', 'friend', 'colleague'
    inner_circle BOOLEAN DEFAULT 0, -- for CRM priority
    
    -- Contact info
    phone TEXT,
    email TEXT,
    telegram_handle TEXT,
    
    -- Tracking
    last_contact_date DATE,
    contact_frequency TEXT,        -- 'weekly', 'monthly', 'quarterly'
    next_scheduled_ping DATE,
    
    -- Context
    birthday DATE,
    important_dates JSON,          -- anniversaries, etc.
    notes TEXT
);

CREATE TABLE relationship_checkins (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,                    -- 'shared' for couple
    
    -- Mood tracking
    faza_mood INTEGER,             -- 1-10
    gaby_mood INTEGER,
    relationship_vibe INTEGER,     -- 1-10
    
    -- Analysis
    topics_discussed JSON,
    friction_points TEXT,
    wins TEXT,
    
    -- Sentiment (AI calculated)
    sentiment_score DECIMAL(3,2),  -- -1.0 to 1.0
    ai_insights TEXT               -- suggestions based on patterns
);

-- ==================== MODULE 4: THE VESSEL ====================

CREATE TABLE blueprint_logs (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,
    
    -- Daily compliance
    date DATE UNIQUE,
    supplements_taken BOOLEAN,
    super_veggie_eaten BOOLEAN,
    nutty_pudding_eaten BOOLEAN,
    exercise_done BOOLEAN,
    
    -- Details
    supplement_list JSON,
    meals_logged JSON,
    water_intake_ml INTEGER,
    
    -- Score
    compliance_score INTEGER       -- calculated: 0-100
);

CREATE TABLE workouts (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,
    
    -- Session
    workout_type TEXT,             -- 'hyperpump', 'cardio', 'recovery'
    location TEXT,                 -- 'empire_fit', 'home', 'outdoor'
    duration_minutes INTEGER,
    
    -- Performance
    total_volume_kg INTEGER,       -- sum of (weight × reps)
    avg_rpe DECIMAL(2,1),          -- rate of perceived exertion
    prs_achieved JSON,             -- personal records
    
    -- Details
    exercises JSON                 -- structured: [{name, sets, reps, weight, rpe}]
);

CREATE TABLE biometrics (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT,
    
    date DATE,
    
    -- Sleep
    sleep_score INTEGER,           -- from wearable
    sleep_hours DECIMAL(3,1),
    deep_sleep_pct DECIMAL(4,1),
    
    -- Recovery
    hrv INTEGER,                   -- heart rate variability
    resting_hr INTEGER,
    recovery_score INTEGER,
    
    -- Other
    weight_kg DECIMAL(4,1),
    body_fat_pct DECIMAL(4,1),
    
    -- Source
    device_source TEXT             -- 'whoop', 'oura', 'manual'
);

CREATE TABLE sobriety_tracker (
    id TEXT PRIMARY KEY,
    owner TEXT,
    habit_type TEXT,               -- 'alcohol', 'nicotine', 'caffeine', 'social_media'
    
    -- Tracking
    start_date DATE,
    last_relapse DATE,
    current_streak_days INTEGER,
    longest_streak_days INTEGER,
    
    -- Relapse log
    relapse_log JSON,              -- [{date, trigger, context}]
    
    -- Motivation
    why_i_started TEXT,
    savings_calculated DECIMAL(10,2)
);
```

### 2.2 Multi-Tenant Query Pattern

```python
# Every query includes owner context
def get_transactions(user_context='faza', include_shared=True):
    """
    user_context: 'faza' | 'gaby'
    include_shared: whether to include 'shared' transactions
    """
    owners = [user_context]
    if include_shared:
        owners.append('shared')
    
    return db.query(
        "SELECT * FROM transactions WHERE owner IN (?) ORDER BY timestamp DESC",
        owners
    )
```

---

## 3. API Architecture

### 3.1 Structure
```
/api/v1/
├── auth/              # Authentication
│   └── verify         # Cloudflare Access token verification
│
├── bag/               # MODULE 1: Finance
│   ├── transactions
│   ├── budgets
│   ├── subscriptions
│   └── runway         # Calculate days of survival
│
├── brain/             # MODULE 2: Knowledge
│   ├── entries
│   ├── search         # Semantic search via Qdrant
│   ├── worktrees
│   └── srs            # Anki export
│
├── circle/            # MODULE 3: Social
│   ├── health-logs    # Gaby Protocol
│   ├── contacts       # CRM
│   ├── checkins       # Relationship tracking
│   └── sentiment      # Analysis endpoint
│
├── vessel/            # MODULE 4: Health
│   ├── blueprint      # Daily compliance
│   ├── workouts
│   ├── biometrics
│   └── sobriety
│
└── sync/              # Cross-module
    ├── dashboard      # Unified view
    ├── tags           # Global tag search (#bali2026)
    └── contextual     # God-mode insights
```

### 3.2 Authentication
```python
# Every request includes user from Cloudflare Access
headers = {
    "CF-Access-Authenticated-User-Email": "fazaasro@gmail.com"
}

# API maps email to user_id
USER_MAP = {
    "fazaasro@gmail.com": "faza",
    "gabriela.servitya@gmail.com": "gaby"
}
```

---

## 4. Integration Architecture

### 4.1 Event Bus (n8n)

All modules emit events for cross-cutting concerns:

```javascript
// Event format
{
  "event": "transaction.created",
  "timestamp": "2026-02-08T22:00:00Z",
  "user": "faza",
  "data": {
    "transaction_id": "txn_123",
    "amount": 50.00,
    "category": "lifestyle",
    "impact_score": 3
  }
}
```

**Event Types:**
- `transaction.created` → Triggers budget alerts, runway recalc
- `health_log.created` → Triggers care_proxy alert if gaby symptom
- `knowledge_entry.created` → Triggers embedding generation
- `workout.completed` → Updates biometrics correlation
- `checkin.created` → Triggers sentiment analysis

### 4.2 Qdrant Integration

```python
# Vector storage for semantic search
COLLECTIONS = {
    "knowledge": {
        "vector_size": 1536,  # OpenAI text-embedding-3-small
        "distance": "Cosine"
    },
    "transactions": {
        # For "what did I spend on food last month?" queries
        "vector_size": 1536,
        "distance": "Cosine"
    },
    "health_patterns": {
        # For correlating symptoms with triggers
        "vector_size": 1536,
        "distance": "Cosine"
    }
}
```

---

## 5. Module Interface Definitions

### 5.1 Module 1: The Bag (Finance)

**Core Class:**
```python
class BagModule:
    def ingest_receipt(self, image_path: str, user: str) -> dict:
        """OCR → Raw JSON → Classify → Store"""
        pass
    
    def calculate_runway(self, user: str) -> dict:
        """Days of survival remaining based on burn rate"""
        pass
    
    def split_bill(self, transaction_id: str, split_type: str) -> dict:
        """Update faza_portion / gaby_portion"""
        pass
    
    def find_subscriptions(self, user: str) -> list:
        """ML pattern detection for recurring charges"""
        pass
```

**Input Channels:**
- WhatsApp: Photo upload
- Telegram: Photo upload
- Manual: API/Form

**Output:**
- SQLite: transactions table
- Qdrant: embeddings for "search my spending"
- Notifications: Budget alerts

### 5.2 Module 2: The Brain (Knowledge)

**Core Class:**
```python
class BrainModule:
    def ingest(self, content: str, source: str, user: str) -> dict:
        """Store + generate embedding"""
        pass
    
    def semantic_search(self, query: str, user: str, filters: dict) -> list:
        """Qdrant vector search"""
        pass
    
    def generate_srs_cards(self, entry_id: str) -> list:
        """Extract fact-answer pairs for Anki"""
        pass
    
    def create_worktree(self, repo: str, branch: str, user: str) -> dict:
        """Git worktree automation"""
        pass
```

**Input Channels:**
- Voice memo → Whisper API → Text
- Markdown files
- Web clips (n8n bookmarklet)
- Chat logs

**Output:**
- SQLite: knowledge_entries
- Qdrant: semantic embeddings
- Anki: SRS card exports

### 5.3 Module 3: The Circle (Social)

**Core Class:**
```python
class CircleModule:
    def log_symptom(self, symptom: dict, logged_by: str) -> dict:
        """Gaby Protocol - log allergy/reflux"""
        pass
    
    def analyze_sentiment(self, chat_log: str) -> dict:
        """Vibe tracking from uploaded chat logs"""
        pass
    
    def check_crm_reminders(self) -> list:
        """Who needs a check-in?"""
        pass
    
    def create_shared_calendar_event(self, event: dict) -> dict:
        """Bali 2026 planning"""
        pass
```

**Input Channels:**
- Symptom logging form
- Chat log uploads
- Calendar integrations

**Output:**
- Health alerts to Faza
- CRM reminders
- Sentiment reports

### 5.4 Module 4: The Vessel (Health)

**Core Class:**
```python
class VesselModule:
    def log_blueprint_compliance(self, day: date, data: dict) -> dict:
        """Daily supplement/meal tracking"""
        pass
    
    def log_workout(self, session: dict) -> dict:
        """Empire Fit tracking"""
        pass
    
    def sync_biometrics(self, device: str) -> dict:
        """Pull from Whoop/Oura"""
        pass
    
    def calculate_bio_age(self, user: str) -> dict:
        """Age reduction algorithm"""
        pass
```

**Input Channels:**
- Wearable APIs
- Manual logging
- Photo upload (meals)

**Output:**
- Compliance scores
- Bio-age estimates
- Habit streaks

---

## 6. Cross-Module Features (God Mode)

### 6.1 Unified Dashboard

```javascript
GET /api/v1/sync/dashboard?user=faza

Response:
{
  "finance": {
    "runway_days": 87,
    "today_spent": 45.50,
    "bali_fund_progress": 0.65
  },
  "knowledge": {
    "entries_this_week": 12,
    "srs_due": 5
  },
  "health": {
    "blueprint_score": 85,
    "sleep_quality": 7.2,
    "workout_streak": 4
  },
  "social": {
    "gaby_last_symptom": "2 days ago",
    "checkin_due": "mom"
  },
  "insights": [
    "Poor sleep last 3 nights → Consider delaying major purchases",
    "High stress detected → Schedule rest day"
  ]
}
```

### 6.2 Contextual Engine

```python
class ContextualEngine:
    def generate_insights(self, user: str) -> list:
        """
        Cross-module correlation:
        - Sleep (Vessel) + Focus (Brain) → Productivity forecast
        - Stress (Circle) + Spending (Bag) → Block impulse purchases
        - Exercise (Vessel) + Mood (Circle) → Relationship health
        """
        sleep = vessel.get_recent_sleep(user)
        stress = circle.get_stress_level(user)
        spending = bag.get_recent_spending(user)
        
        insights = []
        if sleep < 6 and spending > 100:
            insights.append("Sleep deprived + High spending → Review purchases tomorrow")
        
        return insights
```

### 6.3 Global Tagging

```python
# #bali2026 pulls from all modules
GET /api/v1/sync/tags/bali2026

{
  "finance": {
    "total_saved": 4500,
    "transactions": [...]
  },
  "knowledge": {
    "research_notes": [...],
    "dnd_lore": [...]
  },
  "social": {
    "shared_itinerary": {...},
    "booking_confirmations": [...]
  },
  "health": {
    "vaccination_status": "pending",
    "travel_insurance": "confirmed"
  }
}
```

---

## 7. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] SQLite schema creation
- [ ] FastAPI skeleton
- [ ] n8n webhook endpoints
- [ ] Cloudflare Access integration

### Phase 2: The Bag (Weeks 2-3)
- [ ] Receipt OCR pipeline
- [ ] Transaction classifier
- [ ] Split bill logic
- [ ] Runway calculator

### Phase 3: The Brain (Weeks 4-5)
- [ ] Knowledge ingestion
- [ ] Qdrant embeddings
- [ ] Semantic search
- [ ] Worktree automation

### Phase 4: The Circle (Weeks 6-7)
- [ ] Gaby Protocol UI
- [ ] Care proxy alerts
- [ ] Sentiment analysis
- [ ] CRM reminders

### Phase 5: The Vessel (Weeks 8-9)
- [ ] Blueprint tracker
- [ ] Empire Fit integration
- [ ] Biometric sync
- [ ] Bio-age engine

### Phase 6: God Mode (Week 10)
- [ ] Unified dashboard
- [ ] Contextual insights
- [ ] Cross-module tags

---

## 8. Security Considerations

### 8.1 Data Isolation
```sql
-- Every query must filter by owner
WHERE owner IN ('faza', 'shared')  -- Faza sees his + shared
WHERE owner IN ('gaby', 'shared')  -- Gaby sees hers + shared
WHERE owner = 'shared'             -- Only shared
```

### 8.2 API Security
- Cloudflare Access JWT verification
- Rate limiting per user
- Audit log every read/write

### 8.3 Secret Management
```bash
# .env file (never commit)
OPENAI_API_KEY=
QDRANT_API_KEY=
CF_API_TOKEN=
TELEGRAM_BOT_TOKEN=
```

---

## 9. Technology Stack

| Layer | Technology |
|-------|------------|
| Database | SQLite (structured) + Qdrant (vectors) |
| API | FastAPI (Python) |
| Automation | n8n |
| OCR | Tesseract / OpenAI Vision |
| Embeddings | OpenAI text-embedding-3-small |
| Frontend | React (later) / HTML+HTMX (MVP) |
| Auth | Cloudflare Access |
| Hosting | VPS (existing AAC) |

---

*Architecture designed for modularity, extensibility, and privacy.*
