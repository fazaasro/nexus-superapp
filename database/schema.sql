-- AAC Database Schema v1.0
-- SQLite with multi-tenant support

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ==================== CORE ====================

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY CHECK (id IN ('faza', 'gaby', 'shared')),
    email TEXT UNIQUE,
    name TEXT,
    timezone TEXT DEFAULT 'Europe/Berlin',
    preferences JSON
);

INSERT OR IGNORE INTO users (id, email, name) VALUES 
    ('faza', 'fazaasro@gmail.com', 'Faza'),
    ('gaby', 'gabriela.servitya@gmail.com', 'Gaby'),
    ('shared', 'couple@zazagaby.online', 'Shared');

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT,
    module TEXT CHECK (module IN ('bag', 'brain', 'circle', 'vessel', 'system')),
    action TEXT,
    entity_type TEXT,
    entity_id TEXT,
    metadata JSON,
    ip_address TEXT
);

-- ==================== MODULE 1: THE BAG ====================

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    created_by TEXT,
    raw_text TEXT,
    source_image TEXT,
    merchant TEXT,
    amount DECIMAL(10,2),
    currency TEXT DEFAULT 'EUR',
    category TEXT CHECK (category IN ('survival', 'health', 'lifestyle', 'trash', 'income', 'investment')),
    impact_score INTEGER CHECK (impact_score BETWEEN 1 AND 5),
    split_type TEXT CHECK (split_type IN ('solo', 'split_equal', 'split_custom')),
    faza_portion DECIMAL(3,2) DEFAULT 1.0 CHECK (faza_portion BETWEEN 0 AND 1),
    gaby_portion DECIMAL(3,2) DEFAULT 0.0 CHECK (gaby_portion BETWEEN 0 AND 1),
    is_business BOOLEAN DEFAULT 0,
    client TEXT,
    tags JSON,
    location TEXT,
    payment_method TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_transactions_owner ON transactions(owner);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_tags ON transactions(tags);

CREATE TABLE IF NOT EXISTS budgets (
    id TEXT PRIMARY KEY,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    name TEXT,
    category TEXT,
    amount DECIMAL(10,2),
    period TEXT CHECK (period IN ('weekly', 'monthly', 'yearly')),
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    merchant TEXT,
    amount DECIMAL(10,2),
    frequency TEXT CHECK (frequency IN ('weekly', 'monthly', 'quarterly', 'yearly')),
    next_payment DATE,
    category TEXT,
    is_essential BOOLEAN DEFAULT 0,
    cancellation_url TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'paused'))
);

-- ==================== MODULE 2: THE BRAIN ====================

CREATE TABLE IF NOT EXISTS knowledge_entries (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    created_by TEXT,
    title TEXT,
    content TEXT,
    content_type TEXT CHECK (content_type IN ('note', 'voice_transcript', 'web_clip', 'code', 'pdf_extract')),
    source_url TEXT,
    source_file TEXT,
    domain TEXT CHECK (domain IN ('tech', 'dnd', 'masters', 'life', 'finance', 'health')),
    project TEXT,
    tags JSON,
    is_srs_eligible BOOLEAN DEFAULT 0,
    srs_card_id TEXT,
    qdrant_id TEXT,
    embedding_synced BOOLEAN DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_knowledge_owner ON knowledge_entries(owner);
CREATE INDEX IF NOT EXISTS idx_knowledge_domain ON knowledge_entries(domain);
CREATE INDEX IF NOT EXISTS idx_knowledge_project ON knowledge_entries(project);
CREATE INDEX IF NOT EXISTS idx_knowledge_qdrant ON knowledge_entries(qdrant_id);

CREATE TABLE IF NOT EXISTS worktrees (
    id TEXT PRIMARY KEY,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    repo_name TEXT,
    branch_name TEXT,
    worktree_path TEXT,
    status TEXT CHECK (status IN ('active', 'archived', 'merged')),
    last_accessed DATETIME,
    context_notes TEXT
);

-- ==================== MODULE 3: THE CIRCLE ====================

CREATE TABLE IF NOT EXISTS health_logs (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    logged_by TEXT,
    symptom_type TEXT CHECK (symptom_type IN ('allergy', 'reflux', 'mood', 'energy', 'pain', 'sleep')),
    severity INTEGER CHECK (severity BETWEEN 1 AND 10),
    triggers JSON,
    location TEXT,
    meal_before TEXT,
    stress_level INTEGER CHECK (stress_level BETWEEN 1 AND 10),
    sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 10),
    description TEXT,
    remedy_tried TEXT,
    remedy_effectiveness INTEGER CHECK (remedy_effectiveness BETWEEN 1 AND 10)
);

CREATE INDEX IF NOT EXISTS idx_health_owner ON health_logs(owner);
CREATE INDEX IF NOT EXISTS idx_health_symptom ON health_logs(symptom_type);
CREATE INDEX IF NOT EXISTS idx_health_timestamp ON health_logs(timestamp);

CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    name TEXT,
    relationship TEXT CHECK (relationship IN ('family', 'friend', 'colleague', 'mentor', 'other')),
    inner_circle BOOLEAN DEFAULT 0,
    phone TEXT,
    email TEXT,
    telegram_handle TEXT,
    last_contact_date DATE,
    contact_frequency TEXT CHECK (contact_frequency IN ('weekly', 'biweekly', 'monthly', 'quarterly')),
    next_scheduled_ping DATE,
    birthday DATE,
    important_dates JSON,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS relationship_checkins (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT DEFAULT 'shared',
    faza_mood INTEGER CHECK (faza_mood BETWEEN 1 AND 10),
    gaby_mood INTEGER CHECK (gaby_mood BETWEEN 1 AND 10),
    relationship_vibe INTEGER CHECK (relationship_vibe BETWEEN 1 AND 10),
    topics_discussed JSON,
    friction_points TEXT,
    wins TEXT,
    sentiment_score DECIMAL(3,2),
    ai_insights TEXT
);

-- ==================== MODULE 4: THE VESSEL ====================

CREATE TABLE IF NOT EXISTS blueprint_logs (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    date DATE UNIQUE,
    supplements_taken BOOLEAN,
    super_veggie_eaten BOOLEAN,
    nutty_pudding_eaten BOOLEAN,
    exercise_done BOOLEAN,
    supplement_list JSON,
    meals_logged JSON,
    water_intake_ml INTEGER,
    compliance_score INTEGER CHECK (compliance_score BETWEEN 0 AND 100)
);

CREATE INDEX IF NOT EXISTS idx_blueprint_owner ON blueprint_logs(owner);
CREATE INDEX IF NOT EXISTS idx_blueprint_date ON blueprint_logs(date);

CREATE TABLE IF NOT EXISTS workouts (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    workout_type TEXT CHECK (workout_type IN ('hyperpump', 'cardio', 'recovery', 'mobility')),
    location TEXT,
    duration_minutes INTEGER,
    total_volume_kg INTEGER,
    avg_rpe DECIMAL(2,1),
    prs_achieved JSON,
    exercises JSON
);

CREATE INDEX IF NOT EXISTS idx_workouts_owner ON workouts(owner);
CREATE INDEX IF NOT EXISTS idx_workouts_timestamp ON workouts(timestamp);

CREATE TABLE IF NOT EXISTS biometrics (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner TEXT CHECK (owner IN ('faza', 'gaby', 'shared')),
    date DATE,
    sleep_score INTEGER,
    sleep_hours DECIMAL(3,1),
    deep_sleep_pct DECIMAL(4,1),
    hrv INTEGER,
    resting_hr INTEGER,
    recovery_score INTEGER,
    weight_kg DECIMAL(4,1),
    body_fat_pct DECIMAL(4,1),
    device_source TEXT
);

CREATE INDEX IF NOT EXISTS idx_biometrics_owner ON biometrics(owner);
CREATE INDEX IF NOT EXISTS idx_biometrics_date ON biometrics(date);

CREATE TABLE IF NOT EXISTS sobriety_tracker (
    id TEXT PRIMARY KEY,
    owner TEXT CHECK (owner IN ('faza', 'gaby')),
    habit_type TEXT CHECK (habit_type IN ('alcohol', 'nicotine', 'caffeine', 'social_media', 'gaming', 'other')),
    start_date DATE,
    last_relapse DATE,
    current_streak_days INTEGER DEFAULT 0,
    longest_streak_days INTEGER DEFAULT 0,
    relapse_log JSON,
    why_i_started TEXT,
    savings_calculated DECIMAL(10,2) DEFAULT 0
);

-- ==================== VIEWS ====================

-- Shared expenses view
CREATE VIEW IF NOT EXISTS shared_expenses AS
SELECT 
    t.*,
    (t.amount * t.faza_portion) as faza_share,
    (t.amount * t.gaby_portion) as gaby_share
FROM transactions t
WHERE t.owner = 'shared' OR t.split_type != 'solo';

-- Health correlation view
CREATE VIEW IF NOT EXISTS health_correlations AS
SELECT 
    h.*,
    b.sleep_quality as prev_night_sleep,
    b.hrv as morning_hrv
FROM health_logs h
LEFT JOIN biometrics b ON DATE(h.timestamp) = DATE(b.date)
WHERE h.owner = 'gaby';  -- Gaby Protocol focus

-- Monthly spending summary
CREATE VIEW IF NOT EXISTS monthly_spending AS
SELECT 
    owner,
    strftime('%Y-%m', timestamp) as month,
    category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(impact_score) as avg_impact
FROM transactions
WHERE category != 'income'
GROUP BY owner, strftime('%Y-%m', timestamp), category;
