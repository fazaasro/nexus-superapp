# MEMORY.md - Long-Term Memory

## Recent Updates (2026-02-17)

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
