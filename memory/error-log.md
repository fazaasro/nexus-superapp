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

## 2026-02-17

- 🔧 **cAdvisor invalid storage_driver** — cAdvisor v0.47.2 crashed with "unknown backend storage driver: docker". Root cause: `--storage_driver=docker` is not a valid option. Valid options: <empty>, bigquery, elasticsearch, influxdb, kafka, redis, statsd, stdout. Solution: Remove the storage_driver flag (default empty is fine for Prometheus scraping).
- 🔧 **cAdvisor invalid disable_metrics** — cAdvisor crashed with "unsupported metric 'accelerator' specified". Root cause: "accelerator" is not a valid metric to disable. Valid metrics: advtcp,app,cpu,cpuLoad,cpu_topology,cpuset,disk,diskIO,hugetlb,memory,memory_numa,network,oom_event,percpu,perf_event,process,referenced_memory,resctrl,sched,tcp,udp. Solution: Remove "accelerator" from disabled metrics list.
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