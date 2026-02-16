# MEMORY.md - Long-Term Memory

## Infrastructure (2026-02-08)

### Cloudflare Tunnel + Access Stack

**Architecture:**
```
Internet → Cloudflare Access (SSO) → Cloudflare Tunnel → VPS (localhost) → Docker
```

**Critical config:**
- Docker services must bind to `127.0.0.1:PORT` (not just expose)
- API tokens can't modify tunnel configs - use dashboard or local config
- DNS CNAME must point to `<tunnel-id>.cfargotunnel.com`
- Always check if native service exists before deploying docker version

**Security layers:**
1. Docker: Containers bind to 127.0.0.1
2. Cloudflare Access: SSO required for all subdomains
3. Cloudflare Tunnel: Encrypted outbound connection
4. UFW Firewall: Deny all except SSH + Tailscale

**Access control:**
- Group: ZG
- Allowed: fazaasro@gmail.com, gabriela.servitya@gmail.com
- Auth: Email OTP
- Session: 24 hours

## Communication (2026-02-08)

- Pause and think when things aren't working - don't spin
- Listen carefully to corrections (e.g., "i already have outside docker")
- Ask for clarification instead of assuming

## Coding Agents (2026-02-16)

### Available Tools
- **Kimi CLI** - installed at ~/.local/bin/kimi, default model: kimi-code/kimi-for-coding
- **Claude Code** - installed at ~/.local/bin/claude
- **Codex, OpenCode, Pi** - not installed

### Critical Usage Rules
- **Always use pty:true** when running coding agents (they need a terminal)
- Codex requires a git directory (use `mktemp -d && git init` for scratch work)
- Kimi and Claude Code don't require git repos
- Transparency: always say "spawning Kimi..." or "spawning Claude Code..." before using
- Background mode: use `background:true` for long tasks, get sessionId for monitoring
- Monitor with `process:log` to check progress

### Flags
- **Auto-approve:** Codex `--yolo`, Kimi `-y`, Claude Code `--dangerously-skip-permissions`
- **One-shot:** Kimi `-p`, Claude Code `-p` (non-interactive, exits when done)

### Never
- Start coding agents in ~/clawd/ (they'll read soul docs)
- Checkout branches in ~/Projects/openclaw/ (live instance)

## Memory System (2026-02-16)

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

## Workspace Organization (2026-02-16)

### Root Files (6 core)
- AGENTS.md - agent home and conventions
- SOUL.md - who i am
- IDENTITY.md - identity details
- USER.md - about the human
- TOOLS.md - tools reference
- HEARTBEAT.md - periodic tasks

### Directory Structure
- docs/ - organized by category (architecture/, setup/, status/, implementation/)
- memory/ - daily logs (YYYY-MM-DD.md) + error-log.md
- scripts/ - helper scripts
- skills/ - agent skills
- [other dirs for projects: aac-stack, api, core, data, database, modules, tests]

### Home Directory Organization
- stack/ - docker stack (docs/, scripts/, caddy/, cloudflared/)
- scripts/ - system scripts
- caddy/ - consolidated caddy files (config/, data/, host/)
- certificates/ - caddy-ca.crt
- [other dirs: agents, config, data, google-cloud-sdk, swarm]

## Project Context

### AAC Infrastructure (Layer 0) - Complete
- Tailscale VPN
- Cloudflare Tunnel + Access
- 5 services deployed (Portainer, n8n, Qdrant, Code-Server, Overseer)
- SSO active (faza + gaby)

### Next Project
The Bag (Finance module)

## Infrastructure Reference

### VPS Details
- OS: Ubuntu 22.04 LTS
- Domain: zazagaby.online
- Public IP: 95.111.237.115
- Tailscale IP: 100.117.11.11
- Location: Germany (FRA/CDG)

### Docker Services
| Service | Port | Public URL | Purpose |
|---------|------|------------|---------|
| Portainer | 9000 | admin.zazagaby.online | Container management |
| n8n | 5678 | n8n.zazagaby.online | Workflow automation |
| Qdrant | 6333 | qdrant.zazagaby.online | Vector memory DB |
| Code-Server | 8443 | code.zazagaby.online | Browser IDE |
| Overseer | 8501 | monitor.zazagaby.online | Monitoring dashboard |

### Cloudflare Resources
- Account: levynexus001@gmail.com
- Zone ID: cb7a80048171e671bd14e7ba2ead0623
- Tunnel ID: 8678fb1a-f34e-4e90-b961-8151ffe8d051
- Access Group: a38eae36-eb86-4c98-9278-3fad2d253cfd

### Helper Scripts
Location: ~/.openclaw/workspace/scripts/
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

GitHub, Cloudflare, Docker helpers available.


### Helper Scripts
Location: ~/.openclaw/workspace/scripts/
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

GitHub, Cloudflare, Docker helpers available.

---

**Last Updated: 2026-02-16**

## Cron Jobs (2026-02-16)

- OpenClaw cron scheduler: Enabled
- Store: /home/ai-dev/.openclaw/cron/jobs.json
- Current jobs: 0
- Recommendation: Add hourly QMD update job for automatic reindexing
- Command example: `openclaw cron add --schedule '{"kind":"every","everyMs":3600000}' --payload '{"kind":"systemEvent","text":"Running qmd embed..."}'`
