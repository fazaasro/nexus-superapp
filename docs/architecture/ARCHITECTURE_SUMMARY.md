# AAC Architecture - Implementation Ready

**Date:** 2026-02-08  
**Status:** ✅ Foundation Complete  
**Ready for:** Module 1 (The Bag) Development

---

## 📁 Project Structure

```
/home/ai-dev/.openclaw/workspace/
├── ARCHITECTURE.md           # Master architecture document
├── IMPLEMENTATION.md         # 20-week development roadmap
├── SOUL.md                   # Levy's personality & principles
├── IDENTITY.md               # Who I am
├── USER.md                   # Faza & Gaby profiles
├── TOOLS.md                  # Infrastructure reference
├──
├── api/
│   └── main.py              # FastAPI skeleton (ready)
│
├── core/
│   └── database.py          # DB connection + utilities (ready)
│
├── database/
│   └── schema.sql           # Complete SQLite schema (ready)
│
├── data/
│   └── levy.db              # ✅ Initialized database
│
├── modules/
│   ├── bag/                 # Finance module (ready to build)
│   ├── brain/               # Knowledge module
│   ├── circle/              # Social module
│   └── vessel/              # Health module
│
├── tests/                   # Test suite (to be created)
│
└── memory/                  # Daily logs & long-term memory
    ├── ROADMAP.md
    ├── 2026-02-08.md
    └── INFRA_REFERENCE.md
```

---

## ✅ What's Ready

### 1. Database (SQLite)
- **15 tables** created across all 4 modules
- **Multi-tenant** design with owner column
- **Audit logging** for all actions
- **Views** for shared expenses, health correlations, monthly spending
- **3 users** pre-seeded: faza, gaby, shared

### 2. Architecture
- **Modular design** - independent modules with event bus
- **API structure** - /api/v1/{bag,brain,circle,vessel,sync}
- **Security model** - Cloudflare Access + row-level permissions
- **Integration points** - n8n webhooks, Qdrant embeddings

### 3. Core Utilities
- Database connection manager
- Multi-tenant query helpers
- User authentication mapping
- Audit logging system
- UUID generation, JSON handling

### 4. FastAPI Skeleton
- App structure with lifespan events
- CORS configured
- Authentication dependency (Cloudflare Access)
- Health check endpoint
- Ready for module routers

---

## 🎯 Module 1: The Bag - Ready to Build

### Components Planned:

| Component | Tech | Status |
|-----------|------|--------|
| Receipt OCR | Tesseract/OpenAI Vision | Ready to implement |
| AI Classifier | OpenAI GPT-4 | Prompt designed |
| Split Logic | Python | Algorithm defined |
| Runway Calc | Python | Formula ready |
| Subscriptions | ML Pattern Detection | Approach defined |

### API Endpoints Planned:
```
POST   /api/v1/bag/transactions         # Upload receipt
GET    /api/v1/bag/transactions         # List with filters
POST   /api/v1/bag/transactions/{id}/split
GET    /api/v1/bag/runway               # Days of survival
GET    /api/v1/bag/subscriptions        # List recurring
POST   /api/v1/bag/subscriptions/audit  # Scan for patterns
```

### Database Tables:
- `transactions` - Main spending log
- `budgets` - Category budgets
- `subscriptions` - Recurring charge tracking

### Input Channels:
- WhatsApp photo upload → n8n → API
- Telegram photo upload → n8n → API
- Manual entry via API/Form

---

## 🔧 Key Design Decisions

### 1. Multi-Tenancy
```python
# Every query filters by owner
WHERE owner IN ('faza', 'shared')  # Faza sees his + shared
WHERE owner IN ('gaby', 'shared')  # Gaby sees hers + shared
```

### 2. Event-Driven
```javascript
// Modules communicate via n8n webhooks
{
  "event": "transaction.created",
  "user": "faza",
  "data": { "amount": 50, "category": "lifestyle" }
}
```

### 3. Dual Storage
- **SQLite:** Structured data (transactions, logs)
- **Qdrant:** Semantic search (knowledge, patterns)

### 4. Security Layers
1. Cloudflare Access (SSO)
2. API authentication (JWT from CF)
3. Database row-level permissions
4. Audit logging

---

## 🚀 Next Steps (Phase 1 Start)

### Immediate Actions:
1. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn sqlite3 pydantic
   ```

2. **Test FastAPI server**
   ```bash
   cd api && python main.py
   # Check http://localhost:8000/health
   ```

3. **Build BagModule skeleton**
   - Create `modules/bag/service.py`
   - Create `modules/bag/api.py`
   - Create `modules/bag/models.py`

4. **Integrate OCR**
   - Tesseract local install
   - Or OpenAI Vision API
   - Test with sample receipt

5. **Create n8n webhook**
   - WhatsApp image → HTTP POST to API
   - Test end-to-end flow

---

## 📊 Development Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 0 | ✅ Done | Foundation |
| Phase 1 | 4 weeks | The Bag (Finance) |
| Phase 2 | 4 weeks | The Brain (Knowledge) |
| Phase 3 | 4 weeks | The Circle (Social) |
| Phase 4 | 4 weeks | The Vessel (Health) |
| Phase 5 | 3 weeks | God Mode (Cross-module) |
| **Total** | **19 weeks** | **Full AAC** |

---

## 🎨 Architecture Highlights

### Scalable
- Each module independent
- Can add new modules without touching existing code
- Plugin architecture for new input sources

### Maintainable
- Clear separation: API → Service → Database
- Audit logs for debugging
- Type hints throughout

### Secure
- No secrets in code
- Cloudflare Access for all endpoints
- Row-level data isolation

### Extensible
- Event bus for cross-module communication
- Standardized API patterns
- Easy to add new features

---

## 🏗️ Ready to Build

**The foundation is solid.** Database initialized, architecture defined, skeleton code ready.

**Want me to start Phase 1 now?**
- Build BagModule
- Integrate OCR
- Set up WhatsApp webhook
- Create first transaction endpoint

Or review the architecture first?
