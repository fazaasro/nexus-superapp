# OpenClaw Workspace - Levy (Agent Faza)

**Agent:** Levy (Faza)  
**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Overview

This is the OpenClaw workspace for Levy (Agent Faza), an autonomous AI agent running on a self-hosted VPS infrastructure. The workspace contains agent configuration, skills, modules, and automation tools.

---

## Project Structure

```
/home/ai-dev/.openclaw/workspace/
├── AGENTS.md              # Agent behavior and guidelines
├── TOOLS.md               # Infrastructure reference and commands
├── USER.md                # Who I'm helping
├── SOUL.md                # Agent identity
├── IDENTITY.md            # Agent personality
├── MEMORY.md              # Long-term memory (main session only)
├── HEARTBEAT.md           # Heartbeat checklist
├── README.md              # This file
├── memory/                # Daily memory logs
│   ├── YYYY-MM-DD.md      # Daily notes
│   └── error-log.md       # Error log (always loaded)
├── skills/                # Agent skills
│   ├── README.md          # Skills registry
│   ├── github-ops/        # GitHub operations
│   ├── docker-ops/        # Docker operations
│   ├── cloudflare-ops/    # Cloudflare operations
│   ├── monitoring-ops/    # Monitoring operations
│   ├── google-cloud-ops/  # GCP operations
│   ├── storage-wars-2026/ # Benchmarking skill
│   └── ini-compare/       # INI comparison tool
├── aac-stack/             # Infrastructure stack (submodule)
├── core/                  # Core database access
├── modules/               # Agent modules
│   ├── bag/               # BAG document analysis (OCR)
│   ├── brain/             # Brain module
│   ├── circle/            # Circle module
│   └── vessel/            # Vessel module
├── api/                   # API server
├── database/              # Database schema
├── scripts/               # Helper scripts
├── bin/                   # Binary tools
├── docs/                  # Documentation
└── tests/                 # Test files
```

---

## Core Modules

### BAG Module (Bank Account Garbage)

Location: `modules/bag/`

**Purpose:** Document analysis and extraction from financial documents (BAG statements, receipts, invoices)

**Features:**
- OCR-based document processing (EasyOCR, PaddleOCR)
- Text extraction and classification
- Receipt parsing (Indonesian receipts)
- API server for document analysis

**Dependencies:**
- Python 3.12+
- EasyOCR or PaddleOCR
- Flask/FastAPI for API server

**Setup:**
```bash
# Install EasyOCR
pip install easyocr

# Or install PaddleOCR
./setup_paddleocr.sh

# Run API server
cd api
python bag_server.py
```

---

## Infrastructure

See [aac-stack/](./aac-stack/) for complete infrastructure documentation.

**Quick Links:**
- [VPS Infrastructure](https://github.com/fazaasro/aac-stack)
- [Infrastructure Docs](https://github.com/fazaasro/aac-infrastructure)

---

## Environment Variables

Required environment variables (set in `~/.bashrc` or Docker env):

```bash
# OpenClaw
OPENCLAW_HOME=/home/ai-dev/.openclaw
OPENCLAW_WORKSPACE=/home/ai-dev/.openclaw/workspace

# Cloudflare
CF_API_TOKEN=67685adc08f6a53ed01c79a718f67060e38a7
CF_ZONE_ID=cb7a80048171e671bd14e7ba2ead0623
CF_TUNNEL_ID=8678fb1a-f34e-4e90-b961-8151ffe8d051

# GitHub
GH_TOKEN=<your-github-token>

# Optional: OCR Models
EASYOCR_MODEL_DIR=/path/to/models
PADDLEOCR_MODEL_DIR=/path/to/models
```

---

## Skills Documentation

All skills are documented in `skills/README.md`.

**Available Skills:**
- **github-ops** - Repository management, CI/CD
- **docker-ops** - Docker container management
- **cloudflare-ops** - Tunnel and DNS management
- **monitoring-ops** - System health and metrics
- **google-cloud-ops** - Gmail, Calendar, Drive integration
- **storage-wars-2026** - Backend benchmarking
- **ini-compare** - Configuration comparison

See `skills/README.md` for detailed usage.

---

## Development Workflow

### 1. Session Start

Every session, load these files first:
- `AGENTS.md` - Behavior guidelines
- `USER.md` - Who I'm helping
- `memory/YYYY-MM-DD.md` - Recent context
- `memory/error-log.md` - Learn from mistakes

### 2. Making Changes

1. Edit files in workspace
2. Test changes locally
3. Commit with clear messages
4. Push to GitHub

```bash
cd /home/ai-dev/.openclaw/workspace
git add .
git commit -m "feat: add new feature"
git push
```

### 3. Testing

Run test files before committing:
```bash
python test_end_to_end.py
python test_paddleocr_integration.py
```

---

## Helper Scripts

Location: `scripts/`

Load all helpers:
```bash
source /home/ai-dev/.openclaw/workspace/scripts/helpers.sh
levy-help
```

**Available helpers:**
- `gh-*` - GitHub operations (gh-check, gh-repos, gh-new, etc.)
- `cf-*` - Cloudflare operations (cf-tunnels, cf-route, cf-test, etc.)
- `docker-*` - Docker operations (docker-check, docker-log, docker-restart, etc.)

---

## Git Repository

**URL:** https://github.com/fazaasro/levy-agent (planned)  
**Status:** To be created  
**Branch:** `master` (protected, PRs required)

---

## Services & Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| Agent Gateway | agent.zazagaby.online | OpenClaw agent endpoint |
| Code Server | code.zazagaby.online | Browser IDE |
| n8n | n8n.zazagaby.online | Workflow automation |
| Qdrant | qdrant.zazagaby.online | Vector memory |
| Portainer | admin.zazagaby.online | Container management |
| Overseer | monitor.zazagaby.online | Monitoring dashboard |

See [TOOLS.md](./TOOLS.md) for detailed service information.

---

## Memory Management

### Daily Memory
- File: `memory/YYYY-MM-DD.md`
- Purpose: Raw logs of what happened
- Format: Free-form text, timestamps

### Long-term Memory
- File: `MEMORY.md`
- Purpose: Curated wisdom and insights
- Loading: Only in main session (security)
- Updates: Periodically review daily files and update

### Error Log
- File: `memory/error-log.md`
- Purpose: Learn from mistakes immediately
- Format: `- 🏷️ **Title** — What happened. What to do instead.`
- Categories: 🔧 tool-failure, 🧠 wrong-assumption, 🔄 user-correction, 💡 discovery, ⚠️ gotcha, 🏗️ architecture

---

## CI/CD Pipelines

See [GitHub Workflows](.github/workflows/) for automation.

**Workflows:**
- `ci.yml` - Test, lint, build
- `cd.yml` - Deploy to production

---

## Security

- **Memory protection:** MEMORY.md only loaded in main session
- **External access:** Cloudflare Access (SSO required)
- **Network:** All services behind Cloudflare Tunnel (localhost only)
- **Secrets:** Stored in environment variables, never in code

---

## Troubleshooting

### OCR Not Working
```bash
# Check installation
python -c "import easyocr; print(easyocr.__version__)"

# Test with simple script
python simple_paddle_test.py
```

### Docker Services Down
```bash
# Check all services
docker-check

# Restart specific service
docker-restart n8n

# View logs
docker-log n8n 100
```

### Cloudflare Tunnel Issues
```bash
# Check tunnel status
cf-tunnels

# Restart cloudflared
cf-restart

# View logs
cf-logs
```

---

## Contributing

This is a personal agent workspace. For collaboration, see:
- [aac-infrastructure](https://github.com/fazaasro/aac-infrastructure) - Infrastructure docs
- [aac-stack](https://github.com/fazaasro/aac-stack) - Infrastructure code

---

## License

Internal use only. All rights reserved.

---

*Last updated: 2026-02-18*
