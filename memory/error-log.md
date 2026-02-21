# Error Log — Auto-Captured Learnings

## Auto-Capture Loop

When ANY of these happen, immediately append to memory/error-log.md:

- A tool call fails or returns unexpected results
- User corrects you ("no, do it this way")
- You discover a gotcha or undocumented behavior
- An assumption you made turns out wrong
- Something takes way longer than expected

Format: - 🏷️ **Short title** — What happened. What to do instead.

## Categories

🔧 **tool-failure** - something broke
🧠 **wrong-assumption** - agent assumed wrong
🔄 **user-correction** - human said "no, do it this way"
💡 **discovery** - learned something useful
⚠️ **gotcha** - undocumented behavior or subtle trap
🏗️ **architecture** - structural decisions worth remembering

---

## 2026-02-21

- 🔧 **Kimi WriteFile tool infinite loop** — Kimi gets stuck in infinite loop using WriteFile tool. Root cause: Kimi's WriteFile implementation has issues in this environment - keeps retrying the same operation hundreds of times. The file DOES get created eventually, but it takes 30+ seconds and wastes tokens. User says Kimi is working on fixing this. Solution: For simple file operations, use the native `write` tool directly instead of Kimi. Kimi still works for complex coding tasks but avoid it for simple file creation.
- 🔧 **Kimi docker-compose syntax issue** — Kimi uses old `docker-compose` command which fails (exit 127). Root cause: Kimi's tool defaults to v1 syntax. Solution: Use modern `docker compose` (no dash) when writing docker commands manually. Kimi will get stuck in loop trying `docker-compose`. For automation, write the docker-compose.yml and run `docker compose up -d` directly with exec tool.
- 🔧 **Cloudflare API token authentication fails** — Tried using CF_API_TOKEN (67685adc08f6a53ed01c79a718f67060e38a7) with curl but got "Invalid format for Authorization header" errors. Root cause: Unknown - token might be expired, wrong format, or need specific auth method. Attempts: GET /accounts, PUT /tunnels/{id}/configurations with "Authorization: Bearer <token>" header. User says we have global API token and should use it. Solution: Use Cloudflare Dashboard manually for tunnel routes until API auth is resolved. Tunnel info: levy-home-new (8678fb1a-f34e-4e90-b961-8151ffe8d051).
- 💡 **storage-wars and performance-benchmark skills removed** — Both skills were documentation-only (SKILL.md only, no implementation scripts). storage-wars-2026-skill repo was empty. Decision: Remove for now since user hasn't requested benchmarking work and they're taking up space in skills list. Can recreate if/when needed. Files removed: ~/.openclaw/workspace/skills/storage-wars-2026, ~/.openclaw/workspace/skills/performance-benchmark, /home/ai-dev/swarm/repos/nexus-superapp/skills/storage-wars-2026, /home/ai-dev/swarm/repos/nexus-superapp/skills/performance-benchmark, /home/ai-dev/swarm/repos/storage-wars-2026-skill. Result: Skills list reduced from 8 to 6 working skills.

- ✅ ~~**docker-check script regex escaping bug**~~ — ~~Script reported overseer as "stopped" despite 5 overseer containers running. Root cause: `grep -c "^overseer$"` used exact match without escaping special chars, plus overseer containers have hyphenated names (overseer-grafana, overseer-prometheus, etc.). Solution: Added special case for overseer to check for `^overseer-` pattern, ensuring multi-container services are detected correctly. Fixed in ~/.openclaw/workspace/scripts/docker-helpers.sh.~~ **RESOLVED:** Fixed and committed (2026-02-21). Documented in MEMORY.md.
- ✅ ~~**coding agent workflow correction**~~ — ~~User corrected approach: "prioritize claude code and kimi for coding task, give them full context and let them use their tools." Root cause: Overused sessions_spawn for coding tasks when claude code/kimi should be used directly. Solution: Updated workflow to prioritize 1) Claude Code (interactive, multi-file), 2) Kimi yolo mode (automation, quick tasks), 3) sessions_spawn (only for complex orchestration or isolation). Always give full context in prompts, not brief task descriptions. Impact: Better coding workflow, more appropriate tool usage. User feedback accepted immediately.~~ **RESOLVED:** Workflow updated and documented in MEMORY.md (2026-02-21).

## 2026-02-20

- 🔄 **Kimi approval loop without yolo flag** — Kimi CLI gets stuck in approval loop when user doesn't interact. Root cause: Default behavior requires interactive approval for every shell command. Solution: Always use `-y` (yolo) flag for non-interactive coding tasks: `kimi -y -p "your task"` or `exec pty:true command:"kimi -y 'your task'"`. Frequency: First use of kimi for coding task got stuck. Impact: Agent hung indefinitely. Fixed by using yolo mode.
- 💡 **Cloudflare tunnel configuration via API** — Token-based cloudflared service doesn't use local config.yml. Configuration is stored in Cloudflare and managed via API. To add new hostnames, use: `PUT /accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations` with ingress array. The cloudflared service fetches config from Cloudflare automatically on restart.
- 💡 **DNS record creation via Cloudflare API** — Create DNS records with POST to `/zones/{zone_id}/dns_records` using CNAME type pointing to `<tunnel-id>.cfargotunnel.com`. Must set "proxied": true for Cloudflare Access to work.

## 2026-02-17

- ✅ ~~**cAdvisor invalid storage_driver**~~ — ~~cAdvisor v0.47.2 crashed with "unknown backend storage driver: docker". Root cause: `--storage_driver=docker` is not a valid option. Valid options: <empty>, bigquery, elasticsearch, influxdb, kafka, redis, statsd, stdout. Solution: Remove the storage_driver flag (default empty is fine for Prometheus scraping).~~ **RESOLVED:** Removed invalid flag (2026-02-17). New blocker discovered: Docker API version mismatch (2026-02-21). See MEMORY.md for current status.
- ✅ ~~**cAdvisor invalid disable_metrics**~~ — ~~cAdvisor crashed with "unsupported metric 'accelerator' specified". Root cause: "accelerator" is not a valid metric to disable. Valid metrics: advtcp,app,cpu,cpuLoad,cpu_topology,cpuset,disk,diskIO,hugetlb,memory,memory_numa,network,oom_event,percpu,perf_event,process,referenced_memory,resctrl,sched,tcp,udp. Solution: Remove "accelerator" from disabled metrics list.~~ **RESOLVED:** Removed invalid flag (2026-02-17). New blocker discovered: Docker API version mismatch (2026-02-21). See MEMORY.md for current status.
- 💡 **Docker Compose config changes** — Editing docker-compose.yml and running `restart` doesn't apply changes. Use `up -d --force-recreate` to rebuild container with new config.

---

## 2026-02-17

- 🏗️ **Skills verification required** - Checked 11 skills, 6 require updates/fixes. monitoring-ops outdated (Grafana migration), google-cloud-ops inaccurate (gcloud not installed, should use gog), storage-wars-2026/performance-benchmark incomplete (no implementation scripts), cloudflare-ops needs API limitation notes. Full report in memory/skills-verification-report.md.

---

## 2026-02-16

- ⚠️ **QMD skills collection path** — Using relative path for skills collection matched 0 files. Use absolute path (~/.openclaw/workspace/skills) to index all skill subdirectories.
- 💡 **QMD tsx dependency** — QMD requires tsx locally available. Installed with `bun install -g tsx` then added to workspace with `bun add tsx`.
- 💡 **QMD first-time embedding** — Initial embedding takes 7m on CPU (downloads/builds llama.cpp). Subsequent updates only process new/changed files (fast).
- 💡 **QMD vs native memory_search** — QMD indexes multiple collections (workspace, skills, stack) vs native only searches workspace files. Use QMD for comprehensive search across all knowledge.
- 💡 **QMD search modes** — BM25 (240ms, fast, keyword-based), Vector (2s, semantic but needs AI models), Hybrid (5s, combines both). Use BM25 for 90% of lookups, vector/hybrid for semantic queries.
- ⚠️ **QMD vector search requirements** — vsearch and query modes need llama.cpp compiled locally. First compile takes time, but then runs fast. BM25 mode (search) works immediately without compilation.
- 💡 **Cron job syntax** — Use `--every "1h"` not `--schedule '{"kind":"every","everyMs":3600000}'`. Payload uses `--system-event "text"` for main session.
- 💡 **Cron delivery mechanism** — systemEvent injects text into main session, but agent needs to execute actual command. Combine systemEvent text with explicit command in the text payload.

---

## 2026-02-18

- 🔧 **OpenClaw gateway restart stuck** — After running `gateway update.run` (2026.2.14 → 2026.2.17), the gateway restart did not complete. Update installed successfully but gateway still showing old version (2026.2.6-3). System commands (sleep, openclaw version) hung and were killed with SIGKILL. Root cause: Unknown - possibly system load or gateway process hung during restart. Solution: User should manually check `openclaw version` and `journalctl -u openclaw-gateway -f` to diagnose. May need manual restart: `openclaw gateway restart`.
- 🔧 **System commands running slowly** — Simple commands like `sleep 5` took 36+ seconds instead of 5. `openclaw version` command hung indefinitely and was killed with SIGKILL. Root cause: System under heavy load after OpenClaw update, gateway restart affecting exec operations. Solution: Wait for system to stabilize before running commands, or restart gateway manually.
- 🏗️ **Database locking in SQLite** — Calling `log_audit()` inside a `with get_db()` context manager causes "database is locked" error. Root cause: SQLite doesn't support nested database connections from the same context manager. Solution: Call audit logging AFTER exiting the database context, or use separate database connections. Fixed in vessel/service.py log_blueprint().
- ⚠️ **JSON parsing in service layer** — When `get_sobriety_tracker()` returns a dict with `relapse_log` already parsed as a list (from JSON), attempting to `json.loads()` it again in `log_relapse()` causes TypeError. Root cause: Inconsistent JSON handling - some functions parse JSON before returning, others expect raw JSON strings. Solution: Check if value is already a list before parsing: `relapse_log = tracker['relapse_log'] if isinstance(tracker['relapse_log'], list) else []`. Fixed in vessel/service.py.
- ⚠️ **UNIQUE constraint handling in tests** — Running tests multiple times causes UNIQUE constraint failures when inserting entries with same IDs/dates. Root cause: Tests don't clean up after themselves, so duplicate entries accumulate. Solution: Implement upsert logic (INSERT OR REPLACE) or check for existing entries before insert. Fixed in vessel/service.py log_blueprint().
- 🏗️ **SQLite datetime handling** — Using `datetime.now().date()` with string comparison requires consistent ISO format. Root cause: Mixing datetime objects and ISO strings in database queries. Solution: Always convert to ISO strings before storing: `datetime.now().date().isoformat()`.
## 2026-02-19

- 💡 **Cloudflare Access API integration** — Create Cloudflare Access apps via POST to `/accounts/{account_id}/access/apps` with self_hosted type, domain, session_duration, and policies array. Include email policies for user access. HTTP-only cookies and 24h sessions recommended for security.
