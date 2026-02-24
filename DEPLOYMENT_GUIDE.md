# Nexus Superapp - Deployment Guide

**Last Updated:** 2026-02-24
**Status:** Ready for Production (75% complete, 100% core features)

---

## Prerequisites

### 1. System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB
- OS: Ubuntu 22.04 LTS (or compatible)

**Recommended:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+
- GPU: Optional (for faster embeddings)

### 2. Software Dependencies

**Required:**
- Python 3.10+
- Docker & Docker Compose
- Node.js 18+ (for QMD if using)
- SQLite 3

**Python Packages:**
```bash
pip install -r requirements.txt
```

**External Services:**
- Qdrant (vector database) - Docker container available
- Cloudflare Tunnel + Access (for secure external access)

---

## Quick Start (Development)

### 1. Clone Repository

```bash
cd ~/swarm/repos
git clone https://github.com/fazaasro/nexus-superapp.git
cd nexus-superapp
```

### 2. Set Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values
vim .env
```

**Required Variables:**
```bash
# JWT Secret (generate with: python -c "import secrets; print(secrets.token_urlsafe(64))")
export SECRET_KEY=your-generated-secret-key-here

# Database
export SQLITE_DB_DIR=./data

# Qdrant (Vector Database)
export QDRANT_HOST=http://127.0.0.1:6333
export QDRANT_KNOWLEDGE_COLLECTION=nexus_knowledge

# AnkiConnect (optional, for flashcard integration)
export ANKICONNECT_URL=http://127.0.0.1:8765
```

**Optional Variables (Google OAuth):**
```bash
export GOOGLE_CLIENT_ID=your-google-client-id
export GOOGLE_CLIENT_SECRET=your-google-client-secret
export GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### 3. Initialize Database

```bash
# Run database schema
sqlite3 data/levy.db < database/schema.sql

# Run authentication migration
sqlite3 data/levy.db < database/migrations/add_auth_fields.sql
```

### 4. Start Qdrant (Vector Database)

```bash
# Option A: Docker (recommended)
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/data/qdrant:/qdrant/storage \
  qdrant/qdrant:latest

# Option B: Use existing Qdrant instance
# Already running at: http://127.0.0.1:6333 (in AAC Stack)
```

### 5. Start API Server

```bash
# Development (auto-reload)
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

# Production (no reload, 4 workers)
uvicorn api.main:app --host 127.0.0.1 --port 8000 --workers 4
```

### 6. Verify Setup

```bash
# Health check
curl http://127.0.0.1:8000/health

# API docs (Swagger UI)
open http://127.0.0.1:8000/docs
```

---

## Production Deployment

### 1. Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  nexus-api:
    build: .
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - QDRANT_HOST=http://qdrant:6333
      - SQLITE_DB_DIR=/app/data
    volumes:
      - ./data:/app/data
    depends_on:
      - qdrant
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "127.0.0.1:6333:6333"
      - "127.0.0.1:6334:6334"
    volumes:
      - ./data/qdrant:/qdrant/storage
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:6333/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2. Create `.env` File

```bash
# Generate secure secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")

# Create .env file
cat > .env << EOF
SECRET_KEY=$SECRET_KEY
QDRANT_HOST=http://qdrant:6333
QDRANT_KNOWLEDGE_COLLECTION=nexus_knowledge
SQLITE_DB_DIR=/app/data
EOF
```

### 3. Initialize Database

```bash
# Create data directory
mkdir -p data

# Initialize database
docker-compose run nexus-api sh -c "sqlite3 /app/data/levy.db < /app/database/schema.sql"
docker-compose run nexus-api sh -c "sqlite3 /app/data/levy.db < /app/database/migrations/add_auth_fields.sql"
```

### 4. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f nexus-api

# Check status
docker-compose ps
```

### 5. Configure Cloudflare Tunnel

Add route to existing Cloudflare Tunnel (`levy-home-new`):

**Option A: Via Dashboard**
1. Go to: https://dash.teams.cloudflare.com/8678fb1a-f34e-4e90-b961-8151ffe8d051/access/tunnels/levy-home-new/connections
2. Click "Public Hostname"
3. Add:
   - Subdomain: `nexus`
   - Service: `http://127.0.0.1:8000`
   - Save

**Option B: Via Config File (NOT SUPPORTED)**
- Cloudflared service uses `--token` flag
- Local config file is ignored
- Must use Dashboard for configuration

**Public URL:** `https://nexus.zazagaby.online`

---

## Cloudflare Access Setup

### 1. Access Policy

**Access Group:** ZG (already exists)
**Members:**
- fazaasro@gmail.com (Faza)
- gabriela.servitya@gmail.com (Gaby)

**Policy:**
- Email OTP authentication
- 24-hour session duration

### 2. Create Policy for Nexus

Go to: https://dash.teams.cloudflare.com/a38eae36-eb86-4c98-9278-3fad2d253cfd/access

**New Policy:**
- Name: Nexus Superapp
- **Include**:
  - Emails: fazaasro@gmail.com, gabriela.servitya@gmail.com
- **Exclude:** None
- Action: Allow

---

## Module-Specific Setup

### Brain Module (Knowledge Management)

**Qdrant Collection:**
- Auto-created on first run
- Name: `nexus_knowledge`
- Vector size: 384 (all-MiniLM-L6-v2)
- Distance: Cosine

**First Run:**
```bash
# Qdrant collection auto-creates when you:
# 1. Create first knowledge entry
# 2. Generate first embedding
# 3. Or run: POST /api/v1/brain/sync/embeddings
```

**Sentence-Transformers Model:**
- Downloads on first use (~500MB)
- Model: `all-MiniLM-L6-v2`
- Cached at: `~/.cache/huggingface/`

### Bag Module (Finance)

**OCR Backends:**

**PaddleOCR (Default - Self-hosted):**
```bash
# Already installed at: ~/.openclaw/workspace/paddle_env2/bin/paddleocr
# Models downloaded on first use
```

**EasyOCR (Self-hosted Service):**
```bash
# Start service if needed (optional)
# docker run -p 127.0.0.1:5000:5000 easyocr/easyocr:latest
```

**OpenAI Vision (Cloud API):**
```bash
# Add to .env
export OPENAI_API_KEY=your-openai-api-key

# Use via API
POST /api/v1/bag/receipts/process
{
  "backend": "openai",
  "image_path": "/path/to/receipt.jpg"
}
```

### Circle Module (Social CRM)

**No external dependencies required**

### Vessel Module (Health Tracking)

**No external dependencies required**

---

## Post-Deployment Checklist

### 1. Verify All Services

```bash
# Check health
curl https://nexus.zazagaby.online/health

# Should return:
{
  "status": "healthy",
  "database": "connected",
  "qdrant": "connected"
}
```

### 2. Test Authentication

```bash
# Register new user
curl -X POST https://nexus.zazagaby.online/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123",
    "name": "Test User"
  }'

# Should return JWT tokens
```

### 3. Test Module Endpoints

```bash
# Test Brain module
curl https://nexus.zazagaby.online/api/v1/brain/entries

# Test Bag module
curl https://nexus.zazagaby.online/api/v1/bag/transactions

# Test Circle module
curl https://nexus.zazagaby.online/api/v1/circle/contacts

# Test Vessel module
curl https://nexus.zazagaby.online/api/v1/vessel/blueprint
```

### 4. Verify Qdrant Integration

```bash
# Create test knowledge entry
curl -X POST https://nexus.zazagaby.online/api/v1/brain/entries \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Entry",
    "content": "This is a test entry for Qdrant integration",
    "domain": "tech"
  }'

# Generate embedding
curl -X POST https://nexus.zazagaby.online/api/v1/brain/entries/test_entry_id/embed \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. Verify OCR Processing

```bash
# Upload test receipt
curl -X POST https://nexus.zazagaby.online/api/v1/bag/receipts/process \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image_path": "/path/to/test-receipt.jpg",
    "backend": "paddleocr"
  }'
```

---

## Monitoring

### 1. Health Checks

**Endpoint:** `GET /health`

**Returns:**
```json
{
  "status": "healthy",
  "database": "connected",
  "qdrant": "connected",
  "timestamp": "2026-02-24T10:00:00Z"
}
```

### 2. Integration with Grafana

**Add to existing Grafana monitoring stack:**

**Dashboard:** Nexus Superapp Health
- API response time
- Database query time
- Qdrant connection status
- OCR processing time
- Error rate

### 3. Logging

**Log Location:** `/var/log/nexus-superapp/`

**Log Rotation:**
- Daily rotation
- Retain 30 days
- Compress old logs

---

## Backup & Recovery

### 1. Database Backup

```bash
# Backup
docker-compose exec nexus-api sh -c "sqlite3 /app/data/levy.db .dump > /backup/levy_backup_$(date +%Y%m%d).sql"

# Restore
docker-compose exec nexus-api sh -c "cat /backup/levy_backup_20260224.sql | sqlite3 /app/data/levy.db"
```

### 2. Qdrant Backup

```bash
# Backup Qdrant data
docker exec qdrant tar -czf /backup/qdrant_backup_$(date +%Y%m%d).tar.gz /qdrant/storage

# Restore
docker exec qdrant tar -xzf /backup/qdrant_backup_20260224.tar.gz -C /
```

### 3. Automated Backups

**Add to cron:**
```bash
# Daily backup at 2 AM
0 2 * * * docker-compose exec nexus-api sh -c "sqlite3 /app/data/levy.db .dump > /backup/levy_backup_$(date +\%Y\%m\%d).sql"
0 2 * * * docker exec qdrant tar -czf /backup/qdrant_backup_$(date +\%Y\%m\%d).tar.gz /qdrant/storage

# Keep last 7 days, delete older
0 3 * * * find /backup -name "*.sql" -mtime +7 -delete
0 3 * * * find /backup -name "*.tar.gz" -mtime +7 -delete
```

---

## Security Considerations

### 1. Secrets Management

**Never commit:**
- `.env` file (in .gitignore)
- API keys
- Passwords

**Rotate regularly:**
- SECRET_KEY (every 6 months)
- Google OAuth credentials (if compromised)
- OpenAI API key (if using)

### 2. Network Security

**All services bind to:**
- `127.0.0.1` (localhost only)

**External access via:**
- Cloudflare Tunnel (encrypted)
- Cloudflare Access (SSO)

**No open ports!**

### 3. Input Validation

**All endpoints validate:**
- User input (Pydantic models)
- SQL injection prevention (parameterized queries)
- XSS protection (FastAPI auto-escaping)

### 4. Authentication

**JWT Security:**
- 7-day access token expiration
- 30-day refresh token expiration
- Secure token storage (httpOnly cookies recommended)
- Token blacklist on logout (future enhancement)

---

## Troubleshooting

### 1. Database Connection Failed

**Error:** `sqlite3.OperationalError: unable to open database file`

**Solution:**
```bash
# Create data directory
mkdir -p data

# Check permissions
chmod 755 data
```

### 2. Qdrant Connection Failed

**Error:** `qdrant_client.http.exceptions.UnexpectedResponse`

**Solution:**
```bash
# Check if Qdrant is running
curl http://127.0.0.1:6333/

# Check logs
docker logs qdrant

# Restart Qdrant
docker restart qdrant
```

### 3. OCR Processing Timeout

**Error:** `Timeout after 60s`

**Solution:**
- Use faster OCR backend (PaddleOCR > EasyOCR)
- Resize images before processing
- Use GPU for PaddleOCR (if available)

### 4. Embedding Generation Slow

**Error:** `Embedding generation taking too long`

**Solution:**
```bash
# Use GPU (if available)
export CUDA_VISIBLE_DEVICES=0

# Or use smaller model
# In code, change to: 'all-MiniLM-L6-v2' (already smallest)
```

### 5. Cloudflare Tunnel Not Working

**Error:** `502 Bad Gateway`

**Solution:**
- Check if API server is running: `docker ps`
- Check Cloudflare Tunnel status: `cloudflared status`
- Verify route exists in Dashboard
- Check service binding: `127.0.0.1:8000`

---

## Performance Tuning

### 1. Database

**SQLite Performance:**
```sql
-- Enable WAL mode (write-ahead logging)
PRAGMA journal_mode = WAL;

-- Increase cache size (default 2MB)
PRAGMA cache_size = -64000;  -- 64MB

-- Optimize query plans
PRAGMA optimize;
```

### 2. Qdrant

**Optimize for production:**
```python
# In service initialization
from qdrant_client import QdrantClient

# Use optimized settings
qdrant = QdrantClient(
    url=qdrant_host,
    prefer_grpc=True,  # Use gRPC for faster queries
    timeout=30
)
```

### 3. API Server

**Uvicorn Workers:**
```bash
# Production: 4-8 workers (2x CPU cores)
uvicorn api.main:app --workers 4

# With gunicorn (better for production)
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000
```

---

## Scaling Considerations

### 1. Horizontal Scaling

**Stateless services:**
- API server (can scale horizontally)
- Multiple instances behind load balancer

**Stateful services:**
- SQLite (not suitable for horizontal scaling)
- Qdrant (can cluster for scale)

### 2. Database Migration

**When to switch from SQLite:**
- >100 concurrent users
- >10GB database size
- Need multi-region deployment

**Recommended alternatives:**
- PostgreSQL (with Postgres extension for vectors)
- MongoDB (with $vectorSearch)
- Qdrant (for pure vector storage)

---

## Next Steps

### 1. Testing

- Create comprehensive test suite
- Integration tests for all modules
- Load testing for performance validation

### 2. Monitoring

- Set up Grafana dashboards
- Configure alerts (Prometheus Alertmanager)
- Log aggregation (ELK/Loki)

### 3. CI/CD

- GitHub Actions for automated testing
- Automated deployment on push to main
- Rollback capability

---

## Support

**Documentation:** https://docs.nexus.zazagaby.online
**Issues:** https://github.com/fazaasro/nexus-superapp/issues
**Email:** support@zazagaby.online

---

*Deployment Guide v1.0 - Updated 2026-02-24*
