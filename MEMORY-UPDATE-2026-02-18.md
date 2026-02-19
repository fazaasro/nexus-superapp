# Memory Update - 2026-02-18 19:36

---

## 🧠 Lessons Learned from Last 3 Days

### Docker & Infrastructure
1. **cAdvisor Configuration Validation**
   - Always check documentation for exact flag values
   - Invalid metrics can cause containers to crash
   - Example: `accelerator` is not a valid cAdvisor v0.47.2 metric

2. **Docker Compose Command Behavior**
   - `restart` does NOT apply configuration changes to running containers
   - Must use `up -d --force-recreate` to rebuild with new config
   - Important: Config changes require full container rebuild

3. **Container Resource Limits**
   - cAdvisor needs privileged mode and device access
   - Memory and CPU limits prevent crashes
   - Check logs when containers restart unexpectedly

### Cloudflare Integration
4. **API Authentication Models**
   - WRONG: API tokens are long-lived like regular tokens
   - RIGHT: Session-based auth expires frequently (15-30 minutes)
   - SOLUTION: Use Cloudflare Access Dashboard for tunnel configuration
   - Don't rely on programmatic tunnel creation

5. **Endpoint Formats**
   - Use correct account ID format (simple, not `2x...` format)
   - Check Cloudflare API documentation for exact URL structure
   - API rate limits apply to token-based auth

### Database & Data Handling
6. **SQLite Connection Context**
   - WRONG: Use nested database connections from same context manager
   - RIGHT: SQLite doesn't support nested connections
   - SOLUTION: Use separate connections or call after exiting context

7. **DateTime Storage**
   - WRONG: Mix datetime objects and ISO strings in database
   - RIGHT: Always convert to ISO strings before storing
   - SOLUTION: `datetime.now().date().isoformat()`

8. **JSON Parsing Consistency**
   - WRONG: Assume all values are raw JSON strings
   - RIGHT: Some functions parse before returning
   - SOLUTION: Check type before parsing: `json.loads() if isinstance(value, str) else value`

9. **UNIQUE Constraint Handling**
   - WRONG: Run tests without cleanup causes duplicate errors
   - RIGHT: Tests don't clean up after themselves
   - SOLUTION: Implement upsert logic or check before insert
   - SOLUTION: `if exists: update else: insert`

### Tooling & Agent Behavior
10. **Kimi CLI Shell Commands**
   - ISSUE: Approval loops with shell commands in PTY mode
   - CAUSE: Interactive approval required for each shell operation
   - SOLUTION: Use Kimi for simple prompts only
   - SOLUTION: Use Claude Code for file operations

11. **Subagent Tracking & Reliability**
   - ISSUE: Subagents complete silently without announcements
   - ISSUE: Subagents may not appear in sessions_list (120m window)
   - ISSUE: Timeout issues on complex tasks
   - SOLUTION: Implement real-time progress updates
   - SOLUTION: Create logging standard for subagents
   - SOLUTION: Use subagent status tracking

12. **Git Secret Scanning**
   - ISSUE: Blocks pushes when secrets found in commits
   - BENEFIT: Protects user from accidentally committing secrets
   - CHALLENGE: Workspace secrets (Google Cloud, OAuth) should be removed first
   - SOLUTION: Use environment variables instead of hardcoding secrets

### QMD & Memory Search
13. **QMD Skills Collection Path**
   - ISSUE: Relative path matched 0 files
   - SOLUTION: Use absolute path (~/.openclaw/workspace/skills)
   - BENEFIT: Indexes all skill subdirectories

14. **QMD Search Modes**
   - BM25: 240ms, fast, keyword-based (90% of lookups)
   - Vector: 2s, semantic, needs AI models
   - Hybrid: 5s, combines both
   - RECOMMENDATION: Use BM25 for 90% of lookups

15. **QMD First-Time Embedding**
   - Initial run takes 7m on CPU (downloads/builds llama.cpp)
   - Subsequent runs only process new/changed files (fast)

16. **QMD Collection Coverage**
   - Multiple collections: workspace, skills, stack
   - Native memory_search only searches workspace files
   - BENEFIT: QMD indexes all knowledge for comprehensive search

17. **Cron Job Syntax**
   - WRONG: Complex schedule format with JSON
   - RIGHT: Use `--every "1h"` for simple intervals
   - RECOMMENDATION: Keep it simple unless exact timing matters

18. **Cron Delivery Mechanism**
   - ISSUE: systemEvent injects text but agent needs to execute command
   - SOLUTION: Combine systemEvent text with explicit command in payload

---

## 🎯 Action Items for Next Sessions

### High Priority
1. **Remove Secrets from Workspace**
   - Delete Google Cloud credentials files
   - Delete OAuth client secret files
   - Delete session JSON files in agents/main/sessions/
   - Create .gitignore rules for secrets
   - Implement environment variable usage

2. **Implement Subagent Status Tracking**
   - Add real-time progress updates for subagents
   - Create logging standard (like SUBAGENT_LOG.md but better)
   - Implement timeout detection and auto-retry
   - Add completion announcements

3. **Fix Git Push Workflow**
   - Check for secrets before committing
   - Use secret scanning in CI/CD pipeline
   - Implement pre-commit hooks
   - Use safe push workflow (dry-run → verify → push)

### Medium Priority
4. **Create Cloudflare-Ops Skill**
   - Common Cloudflare operations (tunnel management, DNS, Access)
   - API wrapper for common tasks
   - Documentation for API limitations

5. **Complete Grafana Dashboard Improvements**
   - Implement missing features (OOM events, security dashboard)
   - Fix container metrics (per-container breakdown)
   - Create OpenClaw metrics endpoint

6. **Create OpenClaw Metrics Endpoint**
   - Add /api/metrics endpoint to OpenClaw Gateway
   - Expose: memory_mb, active_sessions, total_sessions, avg_latency_ms
   - Token usage metrics (if possible)
   - Tool usage frequency (if possible)

### Low Priority
7. **Improve Error Handling**
   - Standardize error logging across all services
   - Implement structured error responses
   - Add retry logic with exponential backoff
   - Document all error codes

8. **Create Deployment Playbook**
   - Step-by-step deployment procedures
   - Rollback procedures for each service
   - Health check scripts
   - Monitoring integration guide

---

## 📊 Tools That Need Attention

1. **Cloudflare API** - Session-based auth, not token-based
2. **Docker Compose** - Command behavior not intuitive
3. **Git Secret Scanner** - Blocks legitimate pushes sometimes
4. **Subagent System** - Tracking and reliability issues
5. **Database ORM** - SQLite-specific limitations
6. **Kimi CLI** - PTY mode approval loops

---

## 🚀 Recent Successes

1. ✅ Grafana Migration Complete
   - 75% of Overseer features implemented
   - 6 dashboards created and loaded
   - All monitoring infrastructure healthy
   - Cloudflare Zero Trust configured

2. ✅ OpenClaw Consolidation Complete
   - Single source of truth created
   - Comprehensive documentation (7 files)
   - Skills registry updated
   - Project registry (19 projects)

3. ✅ Nexus Super App - Modules 1-4 Implemented
   - 22 module files created
   - 62+ tests passing
   - 8,000+ lines of code
   - 15 database tables (multi-tenant)

4. ✅ Nexus Web UI - Responsive Application Created
   - FastAPI + Vue 3 + Vuetify 3
   - 23 new files created
   - 56 API endpoints
   - Mobile-first design with dark mode
   - Real-time updates with Pinia

5. ✅ Nexus Production Deployment
   - 18+ test files created
   - Git repository initialized
   - Docker production configuration
   - Cloudflare tunnel integration configured
   - ZTNA architecture compliance verified

---

*Memory update by Agent Levy (Agent Faza)* 🏗️
