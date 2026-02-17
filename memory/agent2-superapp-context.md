# Agent 2: Super App Implementation Context

## Mission
Continue implementation of the "Super App" - the AAC (Autonomous Agent Cloud) platform. Create a name for this project and continue development using Claude Code.

## Project Context

### What is the AAC?
The AAC is a comprehensive personal OS that levels up Faza and Gaby across four pillars:
- 💰 **The Bag** (Finance) - Expense tracking, budgeting, runway calculation
- 🧠 **The Brain** (Knowledge) - Personal wiki, semantic search, SRS/Anki
- 👥 **The Circle** (Social) - Health tracking for Gaby, CRM, relationship insights
- 💪 **The Vessel** (Health) - Blueprint protocol, workout tracking, bio-age reduction

### Architecture Status

#### ✅ Complete (Foundation)
- Database schema (SQLite) with 15 tables across all 4 modules
- Multi-tenant design (faza, gaby, shared)
- FastAPI skeleton at `/home/ai-dev/.openclaw/workspace/api/main.py`
- Core database utilities at `/home/ai-dev/.openclaw/workspace/core/database.py`
- Audit logging system
- Event-driven architecture (n8n webhooks)
- Dual storage: SQLite (structured) + Qdrant (vectors)

#### 🚧 In Progress
- **Module 1: The Bag** - Ready to build
- **API endpoints** - Defined but not implemented
- **n8n integration** - Webhook endpoints ready, not connected
- **Cloudflare Access** - Auth configured, not integrated

#### 📋 To Do
- Module 2: The Brain
- Module 3: The Circle
- Module 4: The Vessel
- God Mode: Cross-module insights

### Current Code Structure
```
/home/ai-dev/.openclaw/workspace/
├── api/
│   └── main.py              # FastAPI skeleton
├── core/
│   └── database.py          # DB connection + utilities
├── database/
│   └── schema.sql           # Complete SQLite schema
├── data/
│   └── levy.db              # ✅ Initialized database
├── modules/
│   ├── bag/                 # Finance (ready to build)
│   ├── brain/               # Knowledge
│   ├── circle/              # Social
│   └── vessel/              # Health
├── docs/
│   ├── architecture/
│   │   ├── ARCHITECTURE.md  # Full architecture doc
│   │   └── ARCHITECTURE_SUMMARY.md
│   ├── implementation/
│   └── setup/
└── memory/                  # Daily logs + long-term memory
```

### Key Design Principles

#### 1. **Modular Independence**
- Each module (Bag, Brain, Circle, Vessel) is independent
- Modules communicate via Event Bus (n8n webhooks)
- No circular dependencies
- Shared utilities in `core/`

#### 2. **Multi-Tenancy**
```sql
-- Every table has owner column
owner = 'faza'  | 'gaby'  | 'shared'

-- Query pattern
WHERE owner IN ('faza', 'shared')  -- Faza sees his + shared
WHERE owner IN ('gaby', 'shared')  -- Gaby sees hers + shared
```

#### 3. **Event-Driven**
```javascript
// Modules emit events for cross-cutting concerns
{
  "event": "transaction.created",
  "timestamp": "2026-02-08T22:00:00Z",
  "user": "faza",
  "data": {
    "transaction_id": "txn_123",
    "amount": 50.00,
    "category": "lifestyle"
  }
}
```

#### 4. **Dual Storage**
- **SQLite:** Structured data (transactions, logs, biometrics)
- **Qdrant:** Semantic search (knowledge, spending patterns, health correlations)

#### 5. **Security Layers**
1. Cloudflare Access (SSO with Email OTP)
2. API authentication (JWT from CF)
3. Database row-level permissions
4. Audit logging for everything

## Module 1: The Bag (Finance) - Next Priority

### What It Does
- Ingest receipt photos (WhatsApp/Telegram)
- OCR + AI classify transactions
- Auto-split bills (solo/split_equal/split_custom)
- Track subscriptions + ghost hunt
- Calculate runway (days of survival)
- Budget tracking

### API Endpoints (defined, not implemented)
```
POST   /api/v1/bag/transactions         # Upload receipt
GET    /api/v1/bag/transactions         # List with filters
POST   /api/v1/bag/transactions/{id}/split
GET    /api/v1/bag/runway               # Days of survival
GET    /api/v1/bag/subscriptions        # List recurring
POST   /api/v1/bag/subscriptions/audit  # Scan for patterns
```

### Database Tables (ready)
- `transactions` - Main spending log with AI classification
- `budgets` - Category budgets
- `subscriptions` - Recurring charge tracking

### Key Features to Implement

#### 1. **Receipt Ingestion Pipeline**
```python
# Flow:
WhatsApp Photo → n8n Webhook → API → OCR → Classify → Store
```

#### 2. **AI Classifier**
```python
# Use OpenAI GPT-4 Vision for classification
class TransactionClassifier:
    def classify_receipt(self, image_path: str) -> dict:
        """
        Returns:
        {
            'merchant': 'Amazon',
            'amount': 29.99,
            'currency': 'EUR',
            'category': 'lifestyle',
            'impact_score': 3,  # 1-5 (AI calculated)
            'items': [...]
        }
        """
```

#### 3. **Split Logic**
```python
def split_transaction(transaction_id: str, split_type: str, portions: dict):
    """
    split_type: 'solo' | 'split_equal' | 'split_custom'
    portions: {'faza': 0.5, 'gaby': 0.5}  # for custom splits
    """
```

#### 4. **Runway Calculator**
```python
def calculate_runway(user: str) -> dict:
    """
    Returns:
    {
        'days_remaining': 87,
        'burn_rate': 45.50,
        'savings': 4000,
        'monthly_burn': 1365,
        'categories': {
            'survival': 800,
            'lifestyle': 400,
            'trash': 165
        }
    }
    """
```

#### 5. **Subscription Hunter**
```python
# ML pattern detection for recurring charges
# Scan transactions for:
# - Same merchant
# - Similar amount (±10%)
# - Monthly frequency
```

## Infrastructure Context

### Current Services
```
Portainer (9000)   → admin.zazagaby.online
n8n (5678)        → n8n.zazagaby.online
Qdrant (6333)     → qdrant.zazagaby.online
Code-Server (8443) → code.zazagaby.online
Overseer (8501)   → monitor.zazagaby.online
```

### Access Control
- **Cloudflare Access Group:** ZG
- **Users:** fazaasro@gmail.com, gabriela.servitya@gmail.com
- **Auth:** Email OTP
- **Session:** 24 hours

### API Endpoints (planned)
```
/api/v1/auth/verify           # Cloudflare Access token verification
/api/v1/bag/*                 # Finance module
/api/v1/brain/*               # Knowledge module
/api/v1/circle/*              # Social module
/api/v1/vessel/*              # Health module
/api/v1/sync/dashboard        # Unified dashboard
/api/v1/sync/tags/{tag}       # Global tag search
```

## Naming Ideas for the Super App

### Concept 1: "Level Up" Theme
- **LevelOne** - Simple, implies first step to greatness
- **Ascend** - Growth, improvement
- **Elevate** - Rising above
- **Apex** - Reaching the top

### Concept 2: "Personal OS" Theme
- **Nexus** - Central hub
- **Core** - The heart of everything
- **Matrix** - The underlying system
- **System** - Clean, functional

### Concept 3: "Transformation" Theme
- **Morph** - Changing, evolving
- **Evolve** - Constant improvement
- **Transform** - Becoming something better
- **Forge** - Building strength

### Concept 4: "Agent/Assistant" Theme
- **Sidekick** - Always there helping
- **Cohort** - Partner in growth
- **Crew** - Your team
- **Ally** - Fighting alongside you

### Recommendation
**"Nexus"** - Strong, simple, implies central hub. Fits the modular architecture perfectly.

## Success Criteria

### Immediate (Phase 1: The Bag)
- [ ] FastAPI server running and accessible via Cloudflare Access
- [ ] Receipt OCR pipeline functional
- [ ] Transaction classifier working (OpenAI GPT-4 Vision)
- [ ] Basic CRUD endpoints for transactions
- [ ] Runway calculator working
- [ ] WhatsApp webhook connected (via n8n)
- [ ] First successful transaction logged from a receipt photo

### Short-term (Module 1 Complete)
- [ ] Split logic implemented
- [ ] Subscription hunter working
- [ ] Budget tracking functional
- [ ] All API endpoints tested
- [ ] Documentation complete

### Long-term (Full AAC)
- [ ] All 4 modules implemented
- [ ] Cross-module insights (God Mode)
- [ ] Dashboard working
- [ ] Mobile-friendly UI
- [ ] Deployment to production

## Next Steps

1. **Choose a name** for the project
2. **Review existing code**:
   - `/home/ai-dev/.openclaw/workspace/api/main.py`
   - `/home/ai-dev/.openclaw/workspace/core/database.py`
   - `/home/ai-dev/.openclaw/workspace/database/schema.sql`
3. **Build BagModule skeleton**:
   - Create `modules/bag/service.py`
   - Create `modules/bag/api.py`
   - Create `modules/bag/models.py`
4. **Implement receipt OCR**:
   - Try Tesseract first (local, free)
   - Or OpenAI Vision API (better, costs $)
5. **Build transaction classifier**:
   - Use OpenAI GPT-4 Vision
   - Design prompt for classification
6. **Create FastAPI endpoints**:
   - POST /api/v1/bag/transactions
   - GET /api/v1/bag/transactions
   - GET /api/v1/bag/runway
7. **Connect n8n webhook**:
   - Create n8n workflow
   - Test WhatsApp → n8n → API flow
8. **Test end-to-end**:
   - Upload receipt photo
   - Verify classification
   - Check database storage

---

*Use Claude Code for this task. Give it this full context before starting.*
