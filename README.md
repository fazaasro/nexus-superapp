# OpenClaw Workspace - Complete Agent Platform

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.2.17-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Internal-red)

---

## Overview

This is the complete OpenClaw workspace for Levy (Agent Faza), an autonomous AI agent running on a self-hosted VPS infrastructure. The workspace contains agent configuration, skills, modules, documentation, and automation tools.

### Key Features

- 🧠 **Persistent Memory** - Daily logs, long-term memory, error log for continuous learning
- 🔧 **10 Reusable Skills** - GitHub, Docker, Cloudflare, monitoring, and more
- 📚 **Comprehensive Documentation** - Architecture, workflow, deployment, and best practices
- 🚀 **Full Infrastructure** - Docker stack, monitoring, CI/CD, all automated
- 🔍 **Semantic Search** - QMD indexes all knowledge for fast retrieval
- 🛡️ **Secure by Design** - Cloudflare Tunnel + Access, no open ports

---

## Quick Start

### For New Users

1. **Read the documentation in order:**
   - [README.md](#) - This file (overview)
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
   - [WORKFLOW.md](WORKFLOW.md) - How memory, learning, and search work
   - [MEMORY_GUIDE.md](MEMORY_GUIDE.md) - Best practices for memory management
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Setup and installation guide

2. **Set up your environment:**
   - Clone this repository
   - Install dependencies (Docker, Node.js, Bun, Python)
   - Configure environment variables
   - Deploy services

3. **Start using OpenClaw:**
   - Initialize the agent
   - Load skills as needed
   - Configure memory system
   - Set up monitoring

### For Existing Users

- **Quick reference:** [TOOLS.md](TOOLS.md) - Infrastructure and commands
- **Projects:** [PROJECTS.md](PROJECTS.md) - All projects managed by OpenClaw
- **Skills:** [skills/README.md](skills/README.md) - Available skills
- **Agent behavior:** [AGENTS.md](AGENTS.md) - Guidelines and conventions

---

## Project Structure

```
/home/ai-dev/.openclaw/workspace/
├── README.md              # This file (overview)
├── ARCHITECTURE.md        # System architecture and component relationships
├── WORKFLOW.md            # Memory, learning, and search workflow
├── MEMORY_GUIDE.md       # Best practices for memory management
├── DEPLOYMENT.md          # Setup and installation guide
├── PROJECTS.md            # Project registry (all projects)
├── TOOLS.md               # Infrastructure reference and commands
├── AGENTS.md              # Agent behavior and guidelines
├── HEARTBEAT.md           # Heartbeat checklist
├── SOUL.md                # Agent identity
├── IDENTITY.md            # Agent personality
├── USER.md                # Who I'm helping
├── MEMORY.md              # Long-term memory (main session only)
├── .env.example           # Environment variables template
│
├── skills/                # Agent skills
│   ├── README.md          # Skills registry
│   ├── github-ops/        # GitHub operations
│   ├── docker-ops/        # Docker operations
│   ├── cloudflare-ops/    # Cloudflare operations
│   ├── monitoring-ops/    # Monitoring operations
│   ├── google-cloud-ops/  # GCP operations
│   ├── storage-wars-2026/ # Benchmarking skill
│   ├── ini-compare/       # INI comparison tool
│   ├── pdf-reader/       # PDF document analysis
│   ├── performance-benchmark/ # Performance analysis
│   └── claude-skill-dev-guide/ # Skill development guide
│
├── modules/               # Agent modules
│   ├── bag/               # BAG document analysis (OCR)
│   ├── brain/             # Brain module (decision engine)
│   ├── circle/            # Circle module (social memory)
│   └── vessel/            # Vessel module (sobriety tracking)
│
├── memory/                # Memory system
│   ├── YYYY-MM-DD.md      # Daily logs (one per day)
│   └── error-log.md       # Error log (always loaded)
│
├── docs/                  # Documentation
│   ├── architecture/      # Architecture docs
│   ├── implementation/    # Implementation docs
│   ├── setup/             # Setup guides
│   └── status/            # Status reports
│
├── core/                  # Core database access
├── api/                   # API server
├── database/              # Database schema
├── scripts/               # Helper scripts
├── bin/                   # Binary tools
├── tests/                 # Test files
└── aac-stack/             # Infrastructure stack (submodule)
```

---

## Documentation Guide

### For Understanding the System

| Document | Purpose | Read When |
|----------|---------|-----------|
| [README.md](README.md) | Overview of the entire system | First time |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and components | Understanding design |
| [WORKFLOW.md](WORKFLOW.md) | Memory, learning, search workflow | Understanding operations |
| [PROJECTS.md](PROJECTS.md) | All projects and their status | Finding projects |

### For Using the System

| Document | Purpose | Read When |
|----------|---------|-----------|
| [MEMORY_GUIDE.md](MEMORY_GUIDE.md) | Best practices for memory management | Writing memory |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Setup and installation guide | Setting up new instance |
| [TOOLS.md](TOOLS.md) | Infrastructure and commands | Working with infrastructure |
| [skills/README.md](skills/README.md) | Available skills and how to use | Finding skills |

### For Agent Behavior

| Document | Purpose | Read When |
|----------|---------|-----------|
| [AGENTS.md](AGENTS.md) | Agent behavior and guidelines | Every session |
| [USER.md](USER.md) | Who you're helping | Every session |
| [SOUL.md](SOUL.md) | Agent identity | Once |
| [IDENTITY.md](IDENTITY.md) | Agent personality | Once |

### For Reference

| Document | Purpose |
|----------|---------|
| [HEARTBEAT.md](HEARTBEAT.md) | Heartbeat checklist |
| [.env.example](.env.example) | Environment variables template |

---

## Key Concepts

### 1. Memory System

OpenClaw uses a three-layer memory system:

```
Daily Files (memory/YYYY-MM-DD.md)
  → Raw logs of what happened

Error Log (memory/error-log.md)
  → Immediate lessons learned (most important!)

MEMORY.md
  → Curated wisdom and insights
```

**Key principle:** Write it down, don't "mental note". Files survive session restarts, mental notes don't.

See [MEMORY_GUIDE.md](MEMORY_GUIDE.md) for complete guide.

### 2. Skills

Skills are reusable workflows for common tasks:

- **github-ops** - Repository management, CI/CD
- **docker-ops** - Docker container management
- **cloudflare-ops** - Tunnel and DNS management
- **monitoring-ops** - System health and metrics
- **google-cloud-ops** - Gmail, Calendar, Drive integration
- And 5 more...

Each skill has:
- `SKILL.md` - Documentation
- `when_to_use` - When to invoke
- `when_not_to_use` - When NOT to invoke
- `workflows` - Step-by-step procedures

See [skills/README.md](skills/README.md) for complete list.

### 3. QMD (Semantic Search)

QMD indexes all knowledge for fast retrieval:

- **BM25** (~240ms) - Keyword search (90% of lookups)
- **Vector** (~2s) - Semantic search (understands meaning)
- **Hybrid** (~5s) - Combines both

Collections:
- `workspace` - Agent workspace files
- `skills` - Skill documentation
- `stack` - Infrastructure code

See [WORKFLOW.md](WORKFLOW.md) for details.

### 4. Cron vs Heartbeat

**Use Heartbeat when:**
- Multiple checks can batch together
- Timing can drift slightly
- You want conversational context

**Use Cron when:**
- Exact timing matters (9:00 AM sharp)
- Task needs isolation from main session
- One-shot reminders (20 minutes from now)

See [WORKFLOW.md](WORKFLOW.md) for decision tree.

---

## Services & Endpoints

| Service | URL | Purpose | Access |
|---------|-----|---------|--------|
| **OpenClaw Gateway** | agent.zazagaby.online | Agent endpoint | Admin only |
| **Portainer** | admin.zazagaby.online | Container management | Admin only |
| **n8n** | n8n.zazagaby.online | Workflow automation | Admin + User |
| **Qdrant** | qdrant.zazagaby.online | Vector memory | Services only |
| **Code Server** | code.zazagaby.online | Browser IDE | Admin only |
| **Grafana** | monitor.zazagaby.online | Monitoring dashboard | Admin + User |

**Access Control:**
- All services behind Cloudflare Access (SSO required)
- Authentication: Email OTP
- Session Duration: 24 hours
- Allowed users: fazaasro@gmail.com, gabriela.servitya@gmail.com

---

## Getting Started

### Session Start Checklist

Every session, load these files first:

1. **AGENTS.md** - Behavior guidelines
2. **USER.md** - Who you're helping
3. **memory/YYYY-MM-DD.md** - Today + yesterday for context
4. **memory/error-log.md** - Learn from mistakes (ALWAYS!)
5. **IF main session:** MEMORY.md - Long-term context

### Memory System

**Daily Memory:** `memory/YYYY-MM-DD.md`
- Raw logs of what happened
- Write during session

**Error Log:** `memory/error-log.md`
- Immediate lessons learned
- Load EVERY session
- Update IMMEDIATELY on failure

**Long-term Memory:** MEMORY.md
- Curated wisdom and insights
- ONLY in main session (security)
- Update every 2-3 days

### Using Skills

```bash
# Navigate to skill directory
cd ~/.openclaw/workspace/skills/<skill-name>

# Read SKILL.md
cat SKILL.md

# Follow documented workflow
# Use provided tools and commands
```

**Example: Deploy new service**
```bash
# Use docker-ops skill
cd ~/.openclaw/workspace/skills/docker-ops
# Follow workflow in SKILL.md
```

### Searching Knowledge

```bash
# Keyword search (BM25)
qmd search "docker compose up"

# Semantic search (vector)
qmd vsearch "how to deploy a new service"

# Hybrid search
qmd hsearch "grafana monitoring setup"

# Interactive query
qmd query
```

---

## Development Workflow

### 1. Making Changes

```bash
# Edit files in workspace
vim ~/.openclaw/workspace/skills/my-skill/SKILL.md

# Test changes locally
cd ~/.openclaw/workspace/skills/my-skill
# Follow workflow in SKILL.md

# Commit with clear messages
cd ~/.openclaw/workspace
git add .
git commit -m "feat: add new feature to my-skill"
git push
```

### 2. Testing

```bash
# Run test files
cd ~/.openclaw/workspace
python test_end_to_end.py
python test_paddleocr_integration.py

# Test specific module
cd modules/bag
python test_bag.py
```

### 3. Documentation

```bash
# Update documentation
vim ~/.openclaw/workspace/README.md

# Update skill documentation
vim ~/.openclaw/workspace/skills/my-skill/SKILL.md

# Commit documentation
git add .
git commit -m "docs: update README and skill documentation"
git push
```

---

## Helper Scripts

Location: `scripts/`

Load all helpers:
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

**Available helpers:**

### GitHub (gh-*)
```bash
gh-check      # Auth status
gh-repos      # List repos
gh-new <name> # Create repo
gh-pr         # Create PR
gh-issues     # List issues
gh-issue <title> # Create issue
```

### Cloudflare (cf-*)
```bash
cf-tunnels              # List tunnels
cf-info <id>           # Tunnel info
cf-route <id> <sub>   # Create DNS route
cf-new <name>          # Create tunnel
cf-test <url>          # Test URL
cf-restart             # Restart cloudflared
cf-logs                # View logs
```

### Docker (docker-*)
```bash
docker-running         # List running
docker-all             # List all
docker-log <cont>      # View logs
docker-follow <cont>   # Follow logs
docker-restart <cont>  # Restart
docker-exec <cont>     # Execute
docker-stats           # Show stats
docker-cleanup         # Remove unused
docker-check           # Check AAC services
docker-restart-all     # Restart all
```

---

## Environment Variables

Required environment variables (set in `~/.bashrc` or `.env`):

```bash
# OpenClaw
export OPENCLAW_HOME=/home/ai-dev/.openclaw
export OPENCLAW_WORKSPACE=/home/ai-dev/.openclaw/workspace
export OPENCLAW_CONFIG=/home/ai-dev/.openclaw/config

# Cloudflare
export CF_API_TOKEN=your_cloudflare_api_token
export CF_ZONE_ID=your_zone_id
export CF_TUNNEL_ID=your_tunnel_id

# GitHub
export GH_TOKEN=your_github_token

# Optional: OCR Models
export EASYOCR_MODEL_DIR=/path/to/models
export PADDLEOCR_MODEL_DIR=/path/to/models
```

See [.env.example](.env.example) for complete template.

---

## Modules

### BAG Module (Bank Account Garbage)

**Purpose:** Document analysis and extraction from financial documents

**Features:**
- OCR-based document processing (EasyOCR, PaddleOCR)
- Text extraction and classification
- Receipt parsing (Indonesian receipts)
- API server for document analysis

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

### Brain Module

**Purpose:** Decision engine and reasoning

**Status:** In development

### Circle Module

**Purpose:** Social memory and relationship tracking

**Status:** In development

### Vessel Module

**Purpose:** Sobriety tracking and recovery support

**Features:**
- Sobriety tracker with relapse logging
- Milestone tracking
- Support resource recommendations

**Database:** SQLite (`database/vessel.db`)

---

## Infrastructure

See [aac-stack/](aac-stack/) for complete infrastructure documentation.

**Quick Links:**
- [VPS Infrastructure](https://github.com/fazaasro/aac-stack)
- [Infrastructure Docs](https://github.com/fazaasro/aac-infrastructure)

**Services:**
- Portainer - Container management
- n8n - Workflow automation
- Qdrant - Vector memory
- Code Server - Browser IDE
- Grafana - Monitoring dashboard
- Prometheus - Time-series database

---

## Git Repository

**URL:** https://github.com/fazaasro/levy-agent  
**Branch:** `master` (protected, PRs required)

**Workflow:**
1. Create branch from master
2. Make changes and test
3. Create pull request
4. Code review
5. Merge to master

---

## CI/CD

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
- **No open ports:** UFW firewall denies all except SSH + Tailscale

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

### QMD Search Not Working
```bash
# Rebuild index
qmd build

# Test search
qmd search "test"
```

---

## Contributing

This is a personal agent workspace. For collaboration, see:
- [aac-infrastructure](https://github.com/fazaasro/aac-infrastructure) - Infrastructure docs
- [aac-stack](https://github.com/fazaasro/aac-stack) - Infrastructure code

---

## Roadmap

### Q1 2026
- ✅ Complete infrastructure documentation
- ✅ Deploy Grafana monitoring stack
- ✅ Integrate QMD for semantic search
- 🟡 Complete Nexus Superapp initial setup
- ⏳ Consolidate Levy Agent documentation

### Q2 2026
- ⏳ Complete Nexus Superapp modules
- ⏳ Add alerting to Grafana
- ⏳ Create CI/CD pipelines
- ⏳ Develop multi-agent system

---

## License

Internal use only. All rights reserved.

---

## Support

For issues or questions:
1. Check [MEMORY_GUIDE.md](MEMORY_GUIDE.md) for memory issues
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) for setup issues
3. Check [WORKFLOW.md](WORKFLOW.md) for workflow questions
4. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system questions

---

*Last updated: 2026-02-18*
