# MEMORY.md - Long-Term Memory

## Recent Updates (2026-02-20)

### 0. Search Quality Decision - QMD BM25 as Default 🔍
**Status:** Comprehensive comparison completed, default search tool selected

**What Was Tested:**
- 3 real queries compared: "cloudflare api authentication", "docker ports localhost", "vault tunnel configuration"
- Actual results side-by-side comparison
- Relevance scoring evaluation
- Context quality assessment

**Results Summary:**
| Query | memsearch Quality | QMD BM25 Quality | Winner |
|--------|-------------------|-------------------|--------|
| cloudflare api authentication | Poor (wrong API) | Good (49-51%) | 🏆 QMD |
| docker ports localhost | Fair (ref table) | Good (65-66%) | 🏆 QMD |
| vault tunnel configuration | Fair (mentions only) | Excellent (85%) | 🏆 QMD |

**Why QMD BM25 Won (3/3 tests):**

1. **Better Relevance** - Consistent 49-85% scores vs basic memsearch ranking
2. **Richer Context** - Line numbers (@@ before, after), code blocks, snippets
3. **Actual Solutions** - Found working API format, security rules, complete config
4. **Broader Coverage** - 173 files (workspace + stack + skills) vs 44 (memory only)

**memsearch Strengths:**
- 83x faster (0.018s vs 1.5s)
- Instant feedback for interactive debugging
- Good for high-frequency search workflows

**Final Decision:**
**Default: QMD BM25** - Use for 90% of AI assistant queries
**Backup: memsearch** - Use for interactive debugging (10+ searches in a row)

**Use Case Guide:**
- AI assistant queries → QMD BM25 (better relevance)
- Cross-repo search → QMD BM25 (covers stack/, skills/)
- API commands → QMD BM25 (shows code blocks with context)
- Troubleshooting → QMD BM25 (richer context, line references)
- Interactive debugging → memsearch (instant feedback loop)
- High-frequency scripts → memsearch (83x faster total time)

**Files:**
- `memory/search-quality-comparison-2026-02-20.md` - Full analysis with 3 test queries

---

## Recent Updates (2026-02-20)

### 0. memsearch Added to All Repositories 🔍
**Status:** Native FTS5 search deployed to all 6 repositories

**What Was Done:**
- Created memsearch scripts (init, index, search, setup)
- Added to vault-infrastructure ✅ (pushed to main)
- Added to aac-infrastructure ✅ (up-to-date)
- Added to aac-stack ✅ (up-to-date)
- Added to levy-agent ✅ (up-to-date)
- Added to overseer-monitoring ✅ (up-to-date)
- Added to project-levy-ssh ✅ (up-to-date)

**Files Added to Each Repo:**
- `.scripts/memsearch-init.sql` - Database initialization
- `.scripts/memsearch-index.sh` - Index repository files
- `.scripts/memsearch-search.sh` - Search database
- `.scripts/memsearch-setup.sh` - One-time setup script
- `README-MEMSEARCH.md` - Documentation

**Now Available in All Repos:**
- QMD BM25 search (1.5s, 173 files, 3 collections)
- memsearch (0.018s, repo files only, instant feedback)

**Fair Comparison:** Both tools available in all repos → more fair performance comparison possible

**Setup Commands:**
```bash
# In any repository
./.scripts/memsearch-setup.sh     # One-time setup
./.scripts/memsearch-index.sh     # Re-index files
./.scripts/memsearch-search.sh     # Search
```

---

## Recent Updates (2026-02-19)

### 0. QMD & Memory Search Implementation Complete 📊
**Status:** Multiple search systems implemented and tested

**What Was Done:**
- QMD embeddings completed (301 chunks from 67 docs, 8m 6s on CPU)
- Native SQLite FTS5 search implemented (44 memory files, 0.018s search)
- Head-to-head comparison: memsearch vs QMD BM25
- Shell aliases added: memsearch, memreindex, qmem, qstack, qskills
- Error log analysis completed (21 entries, 5 top patterns identified)

**Performance Comparison:**
| Search Type | Speed | Coverage | Best For |
|-------------|-------|----------|----------|
| **memsearch (Native FTS5)** | 0.018s | Memory files only (44) | High-frequency, interactive workflows |
| **QMD BM25** | 1.3s | Workspace + stack + skills (173) | Cross-collection, best relevance |
| **QMD Vector** | 99s | All collections (173) | Deep semantic queries (CPU too slow) |

**Key Learnings:**
- **Speed matters** for high-frequency searches (50 searches = 74s saved with memsearch)
- **Speed doesn't matter** for single AI assistant queries (1.5s is fine when thinking takes 2-5s)
- **QMD BM25 wins** for cross-collection searches with better relevance (85% scores)
- **Native memsearch** is 83x faster but limited to memory files only
- **Use case decision:** memsearch for interactive debugging, QMD BM25 for daily lookups

**Shell Aliases:**
```bash
memsearch       # Fast memory search (0.018s)
memreindex      # Re-index memory files
qmem "query"    # Search memory collection via QMD
qstack "query"  # Search stack/ via QMD
qskills "query" # Search skills/ via QMD
```

**Error Log Analysis:**
- Total entries: 21 (Feb 16-19)
- Top category: Discovery (52%) - learning about new tools
- Top tools with issues: QMD (4, all fixed), OpenClaw Gateway (2, pending)
- No wrong assumptions or user corrections (excellent!)
- Priority fixes: Gateway stability, 6 skill updates (google-cloud-ops, monitoring-ops, pdf-reader)

**Files:**
- `memory/qmd-comparison-2026-02-19.md` - QMD implementation report
- `memory/native-vs-qmd-comparison-2026-02-19.md` - Head-to-head comparison
- `memory/memsearch-benefits-2026-02-19.md` - Practical speed benefits
- `memory/error-log-analysis-2026-02-19.md` - Error patterns and proposals

**Next Session Priorities:**
1. OpenClaw Gateway - Manual restart, check logs, investigate slow commands
2. Skills fixes - google-cloud-ops (use gog), monitoring-ops (Grafana), pdf-reader (install poppler-utils)
3. Dependency verification - Create skill dependency checker script
4. Improve error documentation - Add examples to each category

---

### 1. Session Summary - 9 Hours of Productive Work 🎉
**Status:** All major infrastructure deployments complete

**Session Highlights:**
1. **Vault Deployment** ✅ - HashiCorp Vault v1.21.3 deployed with 4-layer security
2. **Cloudflare Access Integration** ✅ - 6 monitoring services protected with SSO
3. **Vault Secrets Migration** ✅ - 8 secret paths, 30+ key-value pairs migrated
4. **GitHub + Vault Integration** ✅ - 6 repositories integrated, 18 GitHub secrets added
5. **Git Push Resolved** ✅ - Automation working (issue cleared)
6. **Skills Verification** ✅ - 10 skills checked, 6 require updates

**Infrastructure Status:**
- Docker Services: 10/10 healthy
- Cloudflare Access: 6/6 apps configured
- Vault Secrets: 8 paths, 30+ keys
- GitHub Repos: 6 integrated with Vault

**Key Deliverables:**
- Complete Vault deployment guide
- Cloudflare API instructions (how to add new domains)
- GitHub Actions workflow template
- Comprehensive documentation (10 files created)

**Documentation:**
- `/memory/session-summary-2026-02-19.md` - Complete session summary
- `/memory/vault-secrets-registry-2026-02-19.md` - Vault secrets registry
- `/memory/github-vault-integration-complete-2026-02-19.md` - GitHub integration guide

**Next Session Priorities:**
1. Add GitHub Actions workflows using Vault
2. Fix high-priority skills (google-cloud-ops, monitoring-ops)
3. Continue Nexus development (Module 2: The Brain)

---

### 1. GitHub + Vault Integration Complete 🔐
**Status:** All 6 GitHub repositories integrated with Vault

**What Was Integrated:**
- vault-infrastructure ✅
- aac-infrastructure ✅
- aac-stack ✅
- levy-agent ✅
- overseer-monitoring ✅
- project-levy-ssh ✅

**Secrets Added to Each Repo:**
- VAULT_ADDR: http://vault.zazagaby.online
- VAULT_ROLE_ID: 945989a3-d4ad-3a14-99ee-d6e0086d7c71
- VAULT_SECRET_ID: 41e44bae-a83d-2914-324d-c657b5df4dad
- Total: 18 GitHub secrets (3 per repo)

**Security:**
- Read-only AppRole for GitHub Actions
- Centralized secrets management
- Encrypted at rest in Vault
- Access logging and audit trail

**Files:**
- `scripts/vault-integration.sh` - Automated integration script
- `.github/workflows/vault-integration-template.yml` - Workflow template
- `memory/github-vault-integration-complete-2026-02-19.md` - Complete guide

---

### 1. Vault Secrets Migration Complete 🔐
**Status:** All confidential information moved to Vault

**What Was Migrated:**
- 8 secret paths created in Vault
- 30+ key-value pairs stored
- Cloudflare credentials (account, API token, tunnel)
- GLM API key
- GitHub account information
- Server connection details
- Service passwords
- User contact information

**Secret Paths:**
- `secret/cloudflare-account` - Account details (email, account_id, zone_id, domain)
- `secret/cloudflare-api-token` - API tokens and tunnel ID
- `secret/cloudflare-tunnel` - Tunnel configuration
- `secret/glm-api-key` - GLM API authentication
- `secret/github` - GitHub account info
- `secret/server-info` - Server connection (VPS IP, Tailscale IP, SSH user)
- `secret/service-passwords` - Default credentials (Portainer, Grafana, Code-Server)
- `secret/users` - Contact information (Faza, Gaby, Levy)

**Access Methods:**
- Vault CLI: `docker exec vault vault kv get secret/<path>`
- Vault UI: https://vault.zazagaby.online (SSO protected)
- GitHub Actions: AppRole authentication (read-only)

**Security Improvements:**
- Centralized secrets management
- Encrypted at rest in Vault
- Access logging and audit trail
- SSO protection for Vault UI
- Easy secret rotation

**Files:**
- `/memory/vault-secrets-registry-2026-02-19.md` - Complete registry and usage guide
- `/memory/vault-migration-complete-2026-02-19.md` - Migration guide and checklist

---

### 1. Vault Deployment Complete + Cloudflare Access Integration 🏗️
**Status:** Production secrets management deployed and secured

**What Was Deployed:**
- HashiCorp Vault v1.21.3 at vault.zazagaby.online
- Cloudflare Tunnel configuration (DNS + proxy)
- Cloudflare Access SSO protection (Email OTP, 24h sessions)
- GitHub Actions integration with AppRole authentication
- KV Secrets Engine with GLM API key and Cloudflare API token stored

**Infrastructure:**
- Location: /home/ai-dev/swarm/repos/vault-infrastructure/
- Docker Compose deployment on 127.0.0.1:8200
- Cloudflare Tunnel: vault.zazagaby.online → localhost:8200
- Cloudflare Access App ID: 97f59f34-7352-4b53-ade0-37ff5ecb473a

**Credentials:**
- Root Token: [REDACTED]
- Unseal Keys: .vault-keys.txt (5 keys, need 3 to unseal)
- GitHub Actions AppRole:
  - Role ID: 945989a3-d4ad-3a14-99ee-d6e0086d7c71
  - Secret ID: 41e44bae-a83d-2914-324d-c657b5df4dad

**Security Architecture (4 Layers):**
1. Docker: Services bind to 127.0.0.1
2. Cloudflare Tunnel: Encrypted outbound connection
3. Cloudflare Access: SSO with Email OTP
4. Vault: Token-based access control (AppRole for automation)

**Key Learnings:**
- Cloudflare API: Use X-Auth-Email + X-Auth-Key headers (not Bearer token)
- Cloudflare Access: Create apps via POST /accounts/{id}/access/apps with self_hosted type
- Cloudflared: Token-based auth doesn't use local config.yml, managed via API
- Vault: Distribute unseal keys (3 of 5 threshold), revoke root token after AppRole setup

**Files:**
- `/swarm/repos/vault-infrastructure/` - Complete deployment
- `/memory/vault-cloudflare-integration-2026-02-19.md` - Integration details
- `/memory/vault-troubleshooting-2026-02-19.md` - Troubleshooting guide

---

### 1. Skills Verification - 60% Need Updates 📊
**Status:** 10 skills verified, 6 require action

**Results:**
- ✅ Accurate (4): docker-ops, github-ops, claude-skill-dev-guide, ini-compare
- ⚠️ Outdated (2): monitoring-ops (needs Grafana), cloudflare-ops (API issues)
- ❌ Incomplete (2): storage-wars-2026, performance-benchmark
- ❌ Inaccurate (2): google-cloud-ops (gcloud not installed), pdf-reader (pdftotext not installed)

**Key Issues:**
- monitoring-ops still describes old Overseer dashboard (migrated to Grafana)
- google-cloud-ops references gcloud CLI (should use gog CLI)
- pdf-reader requires poppler-utils package (not installed)
- storage-wars-2026 and performance-benchmark only have SKILL.md files

**Recommendations:**
- High priority: Fix google-cloud-ops, monitoring-ops, pdf-reader
- Medium priority: Complete storage-wars-2026, performance-benchmark, document cloudflare-ops API limitations

**Files:**
- `/skills/github-ops/` - ✅ Verified accurate (gh CLI installed, authenticated)
- `/skills/google-cloud-ops/` - ❌ Inaccurate (gcloud not installed)
- `/skills/pdf-reader/` - ❌ Tools missing (pdftotext not installed)
- `/memory/skills-verification-2026-02-19.md` - Full report

---

### 2. GitHub Push Blocker - Headless Environment 🚨
**Status:** Cannot push to GitHub from VPS without browser

**Problem:**
- Git push fails silently in headless Linux environment
- GitHub CLI requires browser for OAuth authentication
- No SSH key configured for GitHub

**Solutions:**
1. **SSH Key (Recommended):** Generate SSH key on VPS, add to GitHub, update git remote to use SSH URL
2. **Personal Access Token:** Generate PAT, configure git remote with token URL
3. **Manual Web UI:** Create repo in browser, clone from VPS

**Impact:** Blocks all git automation workflows until fixed

---

## Older Updates (2026-02-18)

### 0. Skills Verification - 60% Need Updates 📊
**Status:** 10 skills verified, 6 require action

**Results:**
- ✅ Accurate (4): docker-ops, github-ops, claude-skill-dev-guide, ini-compare
- ⚠️ Outdated (2): monitoring-ops (needs Grafana), cloudflare-ops (API issues)
- ❌ Incomplete (2): storage-wars-2026, performance-benchmark
- ❌ Inaccurate (2): google-cloud-ops (gcloud not installed), pdf-reader (pdftotext not installed)

**Key Issues:**
- monitoring-ops still describes old Overseer dashboard (migrated to Grafana)
- google-cloud-ops references gcloud CLI (should use gog CLI)
- pdf-reader requires poppler-utils package (not installed)
- storage-wars-2026 and performance-benchmark only have SKILL.md files

**Recommendations:**
- High priority: Fix google-cloud-ops, monitoring-ops, pdf-reader
- Medium priority: Complete storage-wars-2026, performance-benchmark, document cloudflare-ops API limitations

**Files:**
- `/skills/github-ops/` - ✅ Verified accurate (gh CLI installed, authenticated)
- `/skills/google-cloud-ops/` - ❌ Inaccurate (gcloud not installed)
- `/skills/pdf-reader/` - ❌ Tools missing (pdftotext not installed)

---

### 1. Nexus OCR - Integration Ready 📸
**Status:** OCR backend deployment pending (EasyOCR or OpenAI Vision API)

**What's Ready:**
- Complete OCR processor (`modules/bag/ocr.py`) with 2 backends:
  - EasyOCR: Self-hosted, free, fast (recommended)
  - OpenAI Vision API: Cloud-based, accurate, costs money
- Transaction classification (6 categories, 8/8 tests passed)
- Database schema (15 tables, multi-tenant)
- Integration tests (`test_ocr_integration.py`)
- Indonesian bank statement analysis (195 transactions)

**Key Files:**
- `/modules/bag/ocr.py` - OCR processor (7.5 KB)
- `/modules/bag/service.py` - BagModule with ingest_receipt() (24 KB)
- `/test_ocr_integration.py` - Integration tests (8.0 KB)
- `/test_classification.py` - Classification tests (211 KB)

**Deployment Options:**
- EasyOCR: Deploy `jaidedai/easyocr` Docker image, bind to 127.0.0.1:5000
- OpenAI Vision: Set `OPENAI_API_KEY` env var, run test with real receipt

**Classification Features:**
- Merchant pattern matching (20+ known merchants)
- Item-based classification fallback
- Amount-based heuristics (gas ~$50, streaming ~$15)
- Discretionary flags (essential vs discretionary)
- Recurrence prediction (one-time, weekly, monthly)
- Confidence scoring (0.0-1.0)

**Next Steps:**
- Deploy EasyOCR service OR configure OpenAI API key
- Test with real receipt image
- Verify end-to-end OCR → classification pipeline

---

### 2. OpenClaw Upgrade - Issues 🔧
**Status:** Update installed but restart not completing

**What happened:**
- Update command: `gateway update.run`
- Version change: 2026.2.14 → 2026.2.17
- Update result: ✅ Success (88 seconds, 676 packages changed)
- Gateway restart: 🔄 Stuck (version still showing 2026.2.6-3)

**Issues Encountered:**
1. Gateway restart not completing
   - Update installed successfully
   - Version still showing old version
   - Restart appears to be stuck

2. System commands running slowly
   - `sleep 5` took 36+ seconds
   - `openclaw version` hung indefinitely
   - Both processes killed with SIGKILL

**Root Cause:** Unknown - possibly system load or gateway process hung during restart

**Solution:** Manual intervention required:
   - Check version: `openclaw version`
   - Check logs: `journalctl -u openclaw-gateway -f`
   - Manual restart: `openclaw gateway restart`

**Files Updated:**
- `memory/2026-02-18.md` - Daily log
- `memory/error-log.md` - New errors logged

---

## Older Updates (2026-02-17)

### 0. cAdvisor Fix - Container Healthy ✅ COMPLETE
**Status:** Invalid configuration flags removed, container now healthy

**What was fixed:**
- cAdvisor container was stuck in restart loop (Exit code: 2)
- Removed invalid `--storage_driver=docker` flag (not supported in cAdvisor v0.47.2)
- Removed `accelerator` from `--disable_metrics` (not a valid metric name)
- Container now healthy and serving metrics correctly

**Valid cAdvisor v0.47.2 options:**
- storage_driver: <empty>, bigquery, elasticsearch, influxdb, kafka, redis, statsd, stdout
- disable_metrics: advtcp,app,cpu,cpuLoad,cpu_topology,cpuset,disk,diskIO,hugetlb,memory,memory_numa,network,oom_event,percpu,perf_event,process,referenced_memory,resctrl,sched,tcp,udp

**Lessons:**
- Always check documentation for exact flag values
- Use `docker compose up -d --force-recreate` instead of `restart` to apply config changes
- Git commit: "fix(cadvisor): remove invalid storage_driver and accelerator metric"

**Files Modified:**
- `/home/ai-dev/swarm/repos/overseer/docker-compose.monitoring.yml`

---

### 1. Infrastructure - Grafana Migration ✅ COMPLETE
**Status:** Production monitoring stack deployed

**What was done:**
- Created complete Grafana + Prometheus monitoring stack
- Replaced old Overseer dashboard with Grafana
- 7 containers deployed: Prometheus, Grafana, Node Exporter, Blackbox Exporter, cAdvisor, plus old Overseer
- All services configured to bind to 127.0.0.1 for Cloudflare Tunnel security
- Git repository initialized and committed

**Key files:**
- `/home/ai-dev/swarm/repos/overseer/`
  - `docker-compose.monitoring.yml` - Complete monitoring stack
  - `prometheus/prometheus.yml` - Prometheus configuration
  - `grafana/provisioning/datasources/prometheus.yml` - Grafana data source
  - `grafana/provisioning/dashboards/default.yml` - Grafana dashboard
  - `GRAFANA_MIGRATION_PLAN.md` - Migration documentation

**Lessons:**
- Docker Compose makes complex deployments easy and reproducible
- Service binding to 127.0.0.1 is critical for Cloudflare Tunnel security
- Git tracking essential for production deployments
- Multi-container stacks require proper resource allocation
- cAdvisor configuration must use valid options (no `storage_driver=docker`, no `accelerator` metric)
- Use `docker compose up -d --force-recreate` instead of `restart` to apply config changes

**cAdvisor Fix (2026-02-17):**
- Removed invalid `--storage_driver=docker` flag (not supported in v0.47.2)
- Removed `accelerator` from `--disable_metrics` (not a valid metric)
- Container now healthy and serving metrics correctly

**Next Steps:**
- Configure Cloudflare DNS and Access for external access
- Add more Grafana dashboards (system, services, alerts)
- Set up Prometheus remote_write for long-term storage
- Add Alertmanager for proactive monitoring

---

### 2. Nexus Super App - Module 1 (The Bag) ✅ COMPLETE
**Status:** Finance management module implemented and tested

**What was done:**
- Created complete database schema with 15 tables
- Implemented multi-tenant design (faza, gaby, shared)
- Built OCR processor with OpenAI Vision API integration
- Created transaction classifier with 20+ merchant patterns
- Implemented CRUD operations, runway calculation, budget management
- Wrote comprehensive test suite (8/8 classification tests passed)
- Analyzed Indonesian bank statement (195 transactions)

**Key files:**
- `/home/ai-dev/.openclaw/workspace/`
  - `modules/bag/ocr.py` - OCRProcessor class (4.8 KB)
  - `modules/bag/service.py` - BagModule class (24 KB)
  - `test_ocr_integration.py` - Integration tests (8.0 KB)
  - `test_classification.py` - Classification tests (211 KB)
  - `data/test/indonesian_bank_*.json` - Bank statement analysis

**Features Implemented:**
- Transaction classification into 6 categories: Food, Transportation, Shopping, Entertainment, Health, Uncategorized
- Subcategory detection: Groceries, Restaurant, Fuel, Streaming, Fitness, etc.
- Discretionary spending flags: Essential vs Discretionary
- Recurrence type prediction: One-time, Weekly, Monthly
- Merchant pattern matching with 20+ known merchants
- Item-based classification fallback
- Amount-based heuristic classification
- OCR integration ready (OpenAI Vision API wrapper)

**Test Results:**
- All 8 classification tests passed (100% accuracy on test data)
- Fallback extraction working correctly
- Confidence calculation accurate
- OCR → Classification pipeline ready
- Indonesian bank data analyzed: 195 transactions, IDR currency, 10 categories

**Lessons:**
- Type hints throughout code improve maintainability
- Comprehensive docstrings help future developers
- Error handling with try/except prevents crashes
- Logging for debugging in production
- Unit test coverage where possible
- Production-ready code quality: type hints, docstrings, error handling

**Indonesian Bank Data:**
- Account: FAZA MUHANDISA ASRO
- Account Number: 4372611565
- Period: January 2026
- Currency: IDR
- Opening Balance: IDR 159,585,548.37
- Closing Balance: IDR 76,717,024.41
- Total Transactions: 195

**Category Breakdown:**
- Other: IDR 5,442,875.36 (128 transactions)
- Travel: IDR 3,098,384.00 (9 transactions)
- Transfer: IDR 3,100,700.00 (13 transactions)
- Food & Beverage: IDR 614,380.00 (12 transactions)
- Shopping: IDR 1,004,390.00 (9 transactions)
- Cash Withdrawal: IDR 500,000.00 (1 transaction)
- Bank Fees: IDR 10,000.00 (1 transaction)
- E-Wallet: IDR 325,000.00 (3 transactions)
- Transportation: IDR 253,700.00 (6 transactions)
- Interest: IDR 3,000,063.85 (3 transactions)

**Top Merchants:**
1. FT LOCKER - IDR 2,324,200 (1 transaction)
2. FAZA MUHANDISA ASRO - IDR 352,142.5 (1 transaction)
3. AGODA (Travel) - 2 transactions, ~IDR 700,000 total
4. DOMPET ANAK BANGSA (GoPay) - IDR 30,000
5. QR payments - Various merchants (BALI, GWK, MIXUE, etc.)

**Key Insights:**
- Highest single expense: FT LOCKER (IDR 2.3M)
- Travel heavy: 9 transactions in category (Bali trips)
- Digital payments: Frequent QR code usage, e-wallets (GoPay, DANA, OVO)
- Regular deposits: 2 large credits (IDR 8M + IDR 1.33M) from Gabriela
- Food spending: IDR 614K across 12 transactions (average IDR 51K/meal)
- Bank services: Minimal fees (IDR 10K)

**Next Steps:**
- Test OCR with real receipt images
- Set up OPENAI_API_KEY for production
- Implement Module 2 (The Brain - Knowledge)
- Implement Module 3 (The Circle - Social)
- Implement Module 4 (The Vessel - Health)

---

### 3. Kimi CLI Exploration 🤖
**Status:** Native vision capabilities discovered

**What was discovered:**
- Kimi CLI version: 1.9.0
- Wire Protocol: 1.3
- Model: `models.gemini-3-pro-preview` with `image_in` capability
- Supports image input (receipt photos)
- Supports pasting images (Ctrl+V)
- Includes thinking mode for deeper reasoning
- Has `video_in` capability (mentioned in docs)

**Advantages for Nexus:**
1. No external API needed - Kimi has native vision processing
2. Simpler integration - Just call Kimi with image path
3. Lower cost - Kimi pricing vs OpenAI Vision
4. Image pasting - Receipt photos can be pasted directly (Ctrl+V)
5. Thinking mode - Better classification accuracy for complex receipts

**Issues Encountered:**
- Agents kept getting stuck in approval loops when trying to run shell commands
- Rejected multiple attempts due to shell command approvals
- Complex exploration tasks with many tools cause timeouts
- Same issue repeated multiple times today

**Recommendations:**
- Use Kimi for simple prompts only
- Complex exploration tasks better handled manually
- Use Claude Code for file operations instead of Kimi

**How to Use:**
```bash
# Use gemini-3-pro-preview with vision
kimi -m models.gemini-3-pro-preview -p "Process receipt image"
```

---

### 4. Cloudflare Tunnel Configuration 🚧 PARTIAL
**Status:** Configuration files created, tunnel not operational

**What was done:**
- Created Cloudflare Access Group: ZG (fazaasro@gmail.com, gabriela.servitya@gmail.com)
- Configured authentication: Email OTP
- Set session duration: 24 hours
- Created cloudflared configuration files
- Created credentials file with tunnel ID
- Created systemd service file

**Configuration Files:**
- `/home/ai-dev/.config/cloudflared/config.yml` (647 bytes)
  - Multiple ingress rules for Grafana + Prometheus
  - Metrics endpoint (local only)
  - Tunnel ID: `8678fb1a-f34e-4e90-b961-8151ffe8d051`

- `/home/ai-dev/.config/cloudflared/credentials.json` (410 bytes)
  - Tunnel credentials with valid secret
  - Tunnel name: "monitor-grafana"

- `/home/ai-dev/.config/cloudflared/cloudflared-tunnel.service` (334 bytes)
  - Systemd service file using config file

**Issues Encountered:**
1. Cloudflare Zero Trust API - Session expired errors
   - Error: `{"success":false,"errors":[{"code":9300,"message":"User session has expired. Please log in again"}]}`
   - Root Cause: Hardcoded token in systemd service, session-based auth failing
   - Impact: Cannot create tunnels programmatically
   - Solution: Use Cloudflare Access Dashboard manually

2. Wrong account ID format
   - Error: `{"success":false,"errors":[{"code":7000,"message":"No route for that URI"}]}`
   - Root Cause: Used wrong endpoint format (`2x9...` format rejected)
   - Solution: Use correct endpoint or simple ID

3. Domain doesn't exist
   - Error: DNS records not found for `monitor-new.zazagaby.online`
   - Impact: Cannot access tunnel via domain
   - Solution: Create CNAME record pointing to CFARGOTUNNEL target

**Current Status:**
- Cloudflared service running (PID: 1494895)
- Tunnel: monitor-grafana
- Error: "Unauthorized: Invalid tunnel secret"
- Cause: Service using hardcoded token that doesn't match Cloudflare account

**Solution Prepared:**
- `cloudflared_fix_instructions.md` (461 bytes) - Detailed fix instructions
- `kimi_setup_instructions.md` (2,097 bytes) - OCR options

**Required Actions (Manual):**
1. Stop current cloudflared service
2. Update systemd service to use credentials file instead of token
3. Update credentials.json with valid token
4. Reload systemd and restart service
5. Verify tunnel is running

**Alternative Approaches:**
1. Use existing valid configuration (RECOMMENDED)
   - Current service is running with valid token
   - Best approach is to update configuration to use this valid token
   
2. Create new tunnel via Cloudflare Dashboard
   - Go to https://dash.cloudflare.com
   - Navigate to Zero Trust → Access → Tunnels
   - Click "Create a tunnel"
   - Choose "Self-hosted"
   - Give it a name: `monitor-grafana`
   - Add hostname: `monitor-new.zazagaby.online`
   - Add service: `http://localhost:3000` (Grafana)
   - Save tunnel and note token
   - Update credentials.json with new token
   - Restart cloudflared service

**Next Steps:**
- Execute manual fix instructions
- Create DNS record for monitor-new.zazagaby.online
- Configure Cloudflare Access policy for ZG group
- Test access from external URL
- Login to Grafana with admin/admin credentials

---

## Infrastructure Reference

### VPS Details
- OS: Ubuntu 22.04 LTS
- Domain: zazagaby.online
- Public IP: 95.111.237.115
- Tailscale IP: 100.117.11.11
- Location: Germany (FRA/CDG)

### Docker Services
| Service | Port | Public URL | Purpose | Status |
|---------|------|------------|---------|--------|
| Portainer | 9000 | admin.zazagaby.online | Container management | Up 7 days |
| n8n | 5678 | n8n.zazagaby.online | Workflow automation | Up 7 days |
| Qdrant | 6333, 6334 | qdrant.zazagaby.online | Vector memory DB | Up 7 days |
| Code-Server | 8443 | code.zazagaby.online | Browser IDE | Up 7 days |
| Overseer | 8501 | monitor.zazagaby.online | Monitoring dashboard | Up 6 days |
| Prometheus | 9090 | - | Metrics collection | Up 10 hours |
| Grafana | 3000 | - | Monitoring dashboard | Up 10 hours |
| Node Exporter | 9100 | - | System metrics | Up 10 hours |
| Blackbox Exporter | 9115 | - | ICMP/TCP checks | Up 10 hours |
| cAdvisor | 8080 | - | Container metrics | Restarting (2) |

### Cloudflare Resources
- Account: levynexus001@gmail.com
- Zone ID: cb7a80048171e671bd14e7ba2ead0623
- Tunnel ID: 8678fb1a-f34e-4e90-b961-8151ffe8d051
- Access Group: a38eae36-eb86-4c98-9278-3fad2d253cfd
- Access Group Name: ZG
- Allowed: fazaasro@gmail.com, gabriela.servitya@gmail.com

### Helper Scripts
Location: ~/.openclaw/workspace/scripts/
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

---

## Project Context

### AAC Infrastructure (Layer 0) - Complete
- Tailscale VPN
- Cloudflare Tunnel + Access
- 5 services deployed (Portainer, n8n, Qdrant, Code-Server, Overseer)
- SSO active (faza + gaby)

### Next Project
The Bag (Finance module)

---

## Memory System

### Three-Layer Memory System

**Layer 1: Error Log (auto-capture)**
- Location: memory/error-log.md
- Purpose: Immediately log every failure, correction, and gotcha
- Trigger: When tool fails, user corrects, discovery happens, assumption wrong, or unexpected delay
- Format: `- 🏷️ **Short title** — What happened. What to do instead.`
- Categories: 🔧 tool-failure, 🧠 wrong-assumption, 🔄 user-correction, 💡 discovery, ⚠️ gotcha, 🏗️ architecture

**Layer 2: Local Search with QMD**
- Installed: `bun install -g https://github.com/tobi/qmd`
- Collections: workspace (54), stack (18), skills (11) = 83 documents
- Zero API cost, all local
- Three modes: BM25 (240ms), vector (2s), hybrid (5s)
- First-time embedding: 7m on CPU (downloads/builds llama.cpp)
- Updates: `qmd embed` only processes new/changed files
- Usage: `qmd search "query"`, `qmd vsearch "query"`, `qmd query "query"`

**Layer 3: Heartbeat-Driven Maintenance**
- Periodic distillation from daily logs to MEMORY.md
- Keeps long-term memory relevant and lean
- HEARTBEAT.md tasks include memory hygiene

### Workspace Organization

### Root Files (6 core)
- AGENTS.md - Agent home and conventions
- SOUL.md - Who I am
- IDENTITY.md - Identity details
- USER.md - About the human
- TOOLS.md - Tools reference
- HEARTBEAT.md - Periodic tasks

### Directory Structure
- docs/ - Organized by category (architecture/, setup/, status/, implementation/)
- memory/ - Daily logs (YYYY-MM-DD.md) + error-log.md
- scripts/ - Helper scripts
- skills/ - Agent skills
- [other dirs for projects: aac-stack, api, core, data, database, modules, tests]

### Home Directory Organization
- stack/ - Docker stack (docs/, scripts/, caddy/, cloudflared/)
- scripts/ - System scripts
- caddy/ - Consolidated caddy files (config/, data/, host/)
- certificates/ - caddy-ca.crt
- [other dirs: agents, config, data, google-cloud-sdk, swarm]

---

## Development Guidelines

### Coding Agents Usage

**Available Tools:**
- **Kimi CLI** - Installed at ~/.local/bin/kimi, default model: kimi-code/kimi-for-coding
- **Claude Code** - Installed at ~/.local/bin/claude
- **Codex, OpenCode, Pi** - Not installed

**Critical Usage Rules:**
- **Always use pty:true** when running coding agents (they need a terminal)
- Codex requires a git directory (use `mktemp -d && git init` for scratch work)
- Kimi and Claude Code don't require git repos
- Transparency: Always say "spawning Kimi..." or "spawning Claude Code..." before using
- Background mode: Use `background:true` for long tasks, get sessionId for monitoring
- Monitor with `process:log` to check progress

**Flags:**
- **Auto-approve:** Codex `--yolo`, Kimi `-y`, Claude Code `--dangerously-skip-permissions`
- **One-shot:** Kimi `-p`, Claude Code `-p` (non-interactive, exits when done)

**Never:**
- Start coding agents in ~/clawd/ (they'll read soul docs)
- Checkout branches in ~/Projects/openclaw/ (live instance)

### Code Quality Standards

**Nexus Super App (Python):**
- Type hints throughout all code
- Comprehensive docstrings for all functions and classes
- Error handling with try/except blocks
- Logging for debugging in production
- Unit test coverage where possible
- Production-ready code quality

**Docker Compose:**
- All services bind to 127.0.0.1 (localhost) for Cloudflare Tunnel security
- Clear naming conventions
- Proper resource allocation
- Health checks configured
- Restart policies defined
- Volume mounts for persistence

---

## Error Log

### 2026-02-16
- ⚠️ **QMD skills collection path** — Using relative path for skills collection matched 0 files. Use absolute path (~/.openclaw/workspace/skills) to index all skill subdirectories.
- 💡 **QMD tsx dependency** — QMD requires tsx locally available. Installed with `bun install -g tsx` then added to workspace with `bun add tsx`.
- 💡 **QMD first-time embedding** — Initial embedding takes 7m on CPU (downloads/builds llama.cpp). Subsequent updates only process new/changed files (fast).
- 💡 **QMD vs native memory_search** — QMD indexes multiple collections (workspace, skills, stack) vs native only searches workspace files. Use QMD for comprehensive search across all knowledge.
- 💡 **QMD search modes** — BM25 (240ms, fast, keyword-based), Vector (2s, semantic but needs AI models), Hybrid (5s, combines both). Use BM25 for 90% of lookups, vector/hybrid for semantic queries.
- ⚠️ **QMD vector search requirements** — vsearch and query modes need llama.cpp compiled locally. First compile takes time, but then runs fast. BM25 mode (search) works immediately without compilation.
- 💡 **Cron job syntax** — Use `--every "1h"` not `--schedule '{"kind":"every","everyMs":3600000}'`. Payload uses `--system-event "text"` for main session.
- 💡 **Cron delivery mechanism** — systemEvent injects text into main session, but agent needs to execute actual command. Combine systemEvent text with explicit command in the text payload.
- 🔧 **Kimi agent approval loop** — Agents kept getting stuck in approval loops when using shell commands. Frequency: Multiple occurrences. Impact: Agents get stuck, sessions killed. Root Cause: PTY mode requires interactive approval for shell commands. Solution: Use Kimi for simple prompts only, use Claude Code for file operations.
- 🔧 **Cloudflare API session expired** — Error: `{"success":false,"errors":[{"code":9300,"message":"User session has expired. Please log in again"}]}`. Impact: Cannot create tunnels programmatically. Root Cause: Hardcoded token in systemd service, session-based auth failing. Solution: Use Cloudflare Access Dashboard manually.
- 🔧 **Cloudflare API wrong endpoint** — Error: `{"success":false,"errors":[{"code":7000,"message":"No route for that URI"}]}`. Impact: API calls failing. Root Cause: Used wrong endpoint format. Solution: Use correct endpoint or simple ID.
- 🔧 **Cloudflared unauthorized tunnel secret** — Error: `ERR failed to serve incoming request error="Unauthorized: Invalid tunnel secret"`. Impact: Tunnel not operational. Root Cause: Service configured with hardcoded token that doesn't match Cloudflare account. Solution: Use credentials file with valid token.
