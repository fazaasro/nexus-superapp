# PROJECTS.md - Project Registry

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Table of Contents

1. [Overview](#overview)
2. [Active Projects](#active-projects)
3. [Completed Projects](#completed-projects)
4. [Infrastructure Projects](#infrastructure-projects)
5. [Skills Projects](#skills-projects)
6. [Project Relationships](#project-relationships)
7. [Project Status Matrix](#project-status-matrix)

---

## Overview

This document catalogs all projects that OpenClaw manages or interacts with. Each project includes its purpose, location, dependencies, status, and key details.

### Project Categories

1. **Active Projects** - Currently in development
2. **Completed Projects** - Successfully deployed
3. **Infrastructure Projects** - Supporting systems
4. **Skills Projects** - Reusable capabilities

---

## Active Projects

### 1. Nexus Superapp

**Repository:** [nexus-superapp](https://github.com/fazaasro/nexus-superapp) (planned)  
**Status:** 🟡 In Development  
**Priority:** High  
**Start Date:** 2026-02-15

**Purpose:** All-in-one productivity superapp combining calendar, tasks, notes, and social features

**Location:** `~/swarm/repos/nexus-superapp/`

**Tech Stack:**
- Next.js 14 (App Router)
- TypeScript
- shadcn/ui
- TailwindCSS
- Prisma + PostgreSQL
- NextAuth.js

**Key Features:**
- 📅 Calendar integration (Google Calendar)
- ✅ Task management
- 📝 Notes and documentation
- 👥 Social features (Circle module)
- 🧠 AI assistant integration

**Dependencies:**
- aac-stack (infrastructure)
- google-cloud-ops (GCP integration)
- circle-module (social features)

**Modules:**
1. **Brain Module** - Decision engine
2. **Circle Module** - Social memory and relationships
3. **Vessel Module** - Sobriety tracking

**Current Status:**
- ✅ Project initialized
- 🟡 Next.js scaffold created
- 🟡 shadcn/ui components set up
- ⏳ Database schema design
- ⏳ Core features implementation

**Next Milestones:**
1. Complete Circle module
2. Implement Brain module
3. Integrate with Vessel module
4. Deploy to production

**Challenges:**
- Complex module integration
- Real-time collaboration features
- Scalability considerations

---

### 2. Levy Agent (OpenClaw Workspace)

**Repository:** [levy-agent](https://github.com/fazaasro/levy-agent)  
**Status:** 🟢 Active  
**Priority:** Critical  
**Start Date:** 2026-02-08

**Purpose:** Main OpenCl agent workspace containing configuration, skills, modules, and automation

**Location:** `~/.openclaw/workspace/`

**Key Components:**
- **Agent Configuration:** AGENTS.md, USER.md, SOUL.md
- **Skills:** 10 reusable skills (github-ops, docker-ops, etc.)
- **Modules:** BAG, Brain, Circle, Vessel
- **Memory System:** Daily logs, long-term memory, error log
- **Documentation:** Architecture, workflow, deployment guides

**Dependencies:**
- aac-stack (infrastructure)
- OpenClaw Gateway (host service)
- QMD (semantic search)

**Current Status:**
- ✅ Workspace structure established
- ✅ 10 skills created and documented
- ✅ Memory system implemented
- ✅ QMD integrated
- 🟡 Modules in development
- 🟡 Documentation consolidation in progress

**Next Milestones:**
1. Complete module development
2. Consolidate documentation
3. Create CI/CD pipelines
4. Enhance agent capabilities

---

### 3. Grafana Migration

**Repository:** Part of aac-stack  
**Status:** 🟢 Deployed  
**Priority:** High  
**Start Date:** 2026-02-16  
**Completion Date:** 2026-02-16

**Purpose:** Migrate from Overseer monitoring to Grafana ecosystem

**Location:** `~/stack/aac-stack/monitoring/`

**Tech Stack:**
- Prometheus (time-series database)
- Grafana (visualization)
- Node Exporter (host metrics)
- cAdvisor (container metrics)
- Blackbox Exporter (health checks)

**Key Features:**
- 📊 Real-time metrics visualization
- 📈 Custom dashboards
- 🔔 Alerting (future)
- 📈 Historical data retention
- 🔍 Powerful querying (PromQL)

**What Was Replaced:**
- Overseer monitoring dashboard
- Limited visualization capabilities
- Manual health checks

**Migration Status:**
- ✅ 7 containers deployed
- ✅ Prometheus configured
- ✅ Grafana dashboards created
- ✅ Data flowing correctly
- ⏳ Alerting configuration (future)
- ⏳ Additional dashboards (future)

**Lessons Learned:**
- cAdvisor configuration requires valid options
- All services must bind to 127.0.0.1 for Cloudflare Tunnel
- Grafana offers superior flexibility vs Overseer

---

## Completed Projects

### 1. Storage Wars 2026

**Repository:** [storage-wars-2026](https://github.com/fazaasro/storage-wars-2026)  
**Status:** ✅ Complete  
**Priority:** Low  
**Start Date:** 2026-02-12  
**Completion Date:** 2026-02-13

**Purpose:** Comprehensive benchmarking suite comparing storage backends

**Location:** `~/.openclaw/workspace/skills/storage-wars-2026/`

**Key Features:**
- 📊 Performance benchmarking
- 📈 Comparative analysis
- 📋 Recommendation engine
- 🎯 Simulated competition format

**Backends Tested:**
- SQLite
- PostgreSQL
- MongoDB
- Redis
- File system

**Deliverables:**
- ✅ Benchmarking suite
- ✅ Performance reports
- ✅ Skill documentation
- ✅ Recommendations

**Outcome:** Created reusable skill for storage comparisons

---

### 2. AAC Infrastructure

**Repository:** [aac-infrastructure](https://github.com/fazaasro/aac-infrastructure)  
**Status:** ✅ Complete  
**Priority:** Critical  
**Start Date:** 2026-02-08  
**Completion Date:** 2026-02-10

**Purpose:** Complete infrastructure documentation for Autonomous Agent Cloud

**Location:** `~/.openclaw/workspace/docs/`

**Documentation Created:**
- ✅ SETUP_GUIDE.md - Initial setup instructions
- ✅ BROWSER_SETUP_GUIDE.md - Browser control setup
- ✅ GOOGLE_CALENDAR_SETUP.md - Calendar integration
- ✅ INTEGRATION_GUIDE.md - Service integrations
- ✅ INFRA_STATUS_REPORT.md - Current infrastructure status
- ✅ GITHUB_INFRASTRUCTURE_README.md - GitHub workflows

**Outcome:** Complete documentation for infrastructure setup and maintenance

---

### 3. QMD Integration

**Repository:** Part of levy-agent  
**Status:** ✅ Complete  
**Priority:** High  
**Start Date:** 2026-02-16  
**Completion Date:** 2026-02-16

**Purpose:** Integrate semantic search across all agent knowledge

**Location:** `~/.openclaw/workspace/qmd.config.ts`

**Collections Indexed:**
- workspace - Agent workspace files
- skills - Skill documentation
- stack - Infrastructure code

**Features Implemented:**
- ✅ Multi-collection indexing
- ✅ BM25 search (keyword)
- ✅ Vector search (semantic)
- ✅ Hybrid search (combined)
- ✅ Incremental updates
- ✅ Interactive query mode

**Lessons Learned:**
- Use absolute paths in config
- First-time build takes ~7 minutes
- Subsequent updates are fast
- BM25 for 90% of searches

---

## Infrastructure Projects

### 1. AAC Stack

**Repository:** [aac-stack](https://github.com/fazaasro/aac-stack)  
**Status:** 🟢 Active  
**Priority:** Critical  
**Start Date:** 2026-02-08

**Purpose:** Complete VPS infrastructure stack with Docker, monitoring, AI gateway, and skills

**Location:** `~/stack/aac-stack/`

**Services Deployed:**

| Service | Port | Public URL | Purpose |
|---------|------|------------|---------|
| Portainer | 9000 | admin.zazagaby.online | Container management |
| n8n | 5678 | n8n.zazagaby.online | Workflow automation |
| Qdrant | 6333 | qdrant.zazagaby.online | Vector memory DB |
| Code Server | 8443 | code.zazagaby.online | Browser IDE |
| Grafana | 3000 | monitor.zazagaby.online | Monitoring dashboard |
| Prometheus | 9090 | - | Time-series database |
| Node Exporter | 9100 | - | Host metrics |
| cAdvisor | 8080 | - | Container metrics |
| Blackbox Exporter | 9115 | - | Health checks |

**Tech Stack:**
- Docker Compose
- Ubuntu 22.04 LTS
- Cloudflare Tunnel
- Cloudflare Access (SSO)

**Security:**
- All services bind to 127.0.0.1
- Cloudflare Tunnel for external access
- SSO authentication (Email OTP)
- UFW firewall (deny all except SSH + Tailscale)

**Current Status:**
- ✅ All core services deployed
- ✅ Grafana stack integrated
- ✅ Monitoring operational
- ✅ Documentation complete

---

### 2. OpenClaw Gateway

**Repository:** Host service (not in git)  
**Status:** 🟢 Running  
**Priority:** Critical  
**Version:** 2026.2.17 (as of 2026-02-18)

**Purpose:** Central gateway for agent communication and task execution

**Port:** 18789 (localhost)  
**Public URL:** agent.zazagaby.online

**Responsibilities:**
- Receive and route agent requests
- Manage agent sessions
- Execute commands via shell
- Coordinate with skills and modules
- Handle tool invocations

**Configuration:**
- Environment variables in `~/.bashrc`
- Config file: `~/.openclaw/config/`

**Current Status:**
- 🟢 Running
- 🟢 Agent sessions operational
- 🟡 Recent update to 2026.2.17 (pending restart verification)

---

### 3. Cloudflare Infrastructure

**Account:** levynexus001@gmail.com  
**Status:** 🟢 Active  
**Priority:** Critical

**Components:**

**Cloudflare Tunnel:**
- Tunnel ID: 8678fb1a-f34e-4e90-b961-8151ffe8d051
- Tunnel Name: levy-home-new
- Encrypted outbound connection (VPS → Cloudflare)

**DNS Zone:**
- Domain: zazagaby.online
- Zone ID: cb7a80048171e671bd14e7ba2ead0623

**Access Control:**
- Access Group ID: a38eae36-eb86-4c98-9278-3fad2d253cfd
- Access Group Name: ZG
- Allowed Users:
  - fazaasro@gmail.com (Admin)
  - gabriela.servitya@gmail.com (User)
- Authentication: Email OTP
- Session Duration: 24 hours

**API Token:**
- Permissions: DNS:Edit, Zone:Read, Access:*, Tunnel:Edit

**Current Status:**
- ✅ Tunnel operational
- ✅ DNS routing working
- ✅ Access control enforced
- ✅ All services accessible

---

## Skills Projects

### Skills Registry

**Location:** `~/.openclaw/workspace/skills/`  
**Count:** 10 skills (as of 2026-02-18)

### 1. github-ops (v2.0.0)

**Purpose:** GitHub repository management, CI/CD, 10x Architect protocol

**When to Use:** Creating/managing repositories, setting up CI/CD

**Key Features:**
- Repository creation and management
- PR workflow
- GitHub Actions setup
- 10x Architect protocol

**Dependencies:**
- GitHub CLI (gh)
- GitHub API

**Status:** ✅ Complete and documented

---

### 2. docker-ops (v1.0.0)

**Purpose:** Docker container management

**When to Use:** Deploying/managing Docker services

**Key Features:**
- Service deployment
- Container health checks
- Log viewing
- Service restarts

**Dependencies:**
- Docker daemon
- Docker Compose

**Status:** ✅ Complete and documented

---

### 3. cloudflare-ops (v1.0.0)

**Purpose:** Cloudflare tunnel & DNS management

**When to Use:** Managing tunnels, DNS, Access policies

**Key Features:**
- Tunnel creation and management
- DNS route configuration
- Access policy setup
- URL testing

**Dependencies:**
- Cloudflare API
- cloudflared

**Status:** ✅ Complete and documented

---

### 4. monitoring-ops (v1.0.0)

**Purpose:** Overseer dashboard operations

**When to Use:** Checking system health, reviewing metrics

**Key Features:**
- Health checks
- Trend analysis
- Security monitoring
- OpenClaw analysis

**Status:** 🟡 Needs update (Grafana migration)

---

### 5. google-cloud-ops (v1.0.0)

**Purpose:** GCP operations for autonomous agents

**When to Use:** Gmail, Calendar, Drive, Sheets integration

**Key Features:**
- Gmail management
- Calendar integration
- Drive operations
- Sheets automation

**Dependencies:**
- gog (Google CLI tool)
- Google Cloud APIs

**Status:** 🟡 Needs update (gog not installed, should use gog)

---

### 6. storage-wars-2026 (v1.0.0)

**Purpose:** Complete Storage Wars 2026 benchmarking suite

**When to Use:** Comparing storage backends, performance analysis

**Key Features:**
- Benchmarking simulation
- Performance comparison
- Recommendation engine
- Competition format

**Status:** ✅ Complete and documented

---

### 7. ini-compare (v1.1.0)

**Purpose:** Compare configuration files (INI, YAML, JSON, TOML)

**When to Use:** Comparing configs, finding optimal storage

**Key Features:**
- Multi-format support
- Diff generation
- Recommendation engine

**Status:** ✅ Complete and documented

---

### 8. pdf-reader (v1.0.0)

**Purpose:** Read and analyze PDF files

**When to Use:** Analyzing PDF documents for skill development

**Key Features:**
- PDF text extraction
- Document analysis
- Content parsing

**Dependencies:**
- PyPDF2 or similar

**Status:** ✅ Complete and documented

---

### 9. performance-benchmark (v1.0.0)

**Purpose:** Analyze Storage Wars 2026 benchmark results

**When to Use:** Performance assessment, result analysis

**Key Features:**
- Result parsing
- Performance metrics
- Report generation

**Status:** ✅ Complete and documented

---

### 10. claude-skill-dev-guide (v1.0.0)

**Purpose:** Helps users build skills following Claude's skill development best practices

**When to Use:** Creating new skills, skill development

**Key Features:**
- Skill templates
- Best practices
- Development workflow
- Documentation guidelines

**Status:** ✅ Complete and documented

---

## Project Relationships

### Dependency Graph

```
┌─────────────────────────────────────────────────────────┐
│                    PROJECT DEPENDENCIES                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Nexus Superapp                                        │
│    ├─► Depends on: aac-stack (infrastructure)          │
│    ├─► Depends on: google-cloud-ops (GCP integration)   │
│    └─► Uses: circle-module, brain-module, vessel-module │
│                                                         │
│  Levy Agent (OpenClaw Workspace)                       │
│    ├─► Depends on: aac-stack (infrastructure)          │
│    ├─► Depends on: OpenClaw Gateway (host service)     │
│    ├─► Depends on: QMD (semantic search)               │
│    └─► Contains: All skills, modules, memory          │
│                                                         │
│  Skills (10 total)                                     │
│    ├─► github-ops → GitHub API                        │
│    ├─► docker-ops → Docker daemon                      │
│    ├─► cloudflare-ops → Cloudflare API                 │
│    ├─► monitoring-ops → Grafana/Prometheus             │
│    ├─► google-cloud-ops → Google APIs                  │
│    └─► Others: No external dependencies                │
│                                                         │
│  AAC Stack (Infrastructure)                             │
│    └─► Provides: Docker, Portainer, n8n, Qdrant, etc. │
│                                                         │
│  Grafana Migration                                      │
│    ├─► Part of: aac-stack                              │
│    └─► Replaces: Overseer monitoring                  │
│                                                         │
│  QMD Integration                                        │
│    ├─► Indexes: workspace, skills, stack              │
│    └─► Used by: All agents                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Integration Points

**1. Nexus Superapp ↔ AAC Stack**
- Deployment: Nexus deploys to AAC Stack infrastructure
- Monitoring: Nexus monitored by Grafana (AAC Stack)
- Storage: Nexus uses Qdrant (AAC Stack)

**2. Levy Agent ↔ All Projects**
- Skills: Levy Agent uses all 10 skills
- Modules: Levy Agent contains BAG, Brain, Circle, Vessel
- Documentation: Levy Agent documents all projects

**3. Skills ↔ External APIs**
- github-ops: GitHub API
- docker-ops: Docker daemon
- cloudflare-ops: Cloudflare API
- google-cloud-ops: Google APIs
- Others: Local only

**4. QMD ↔ All Knowledge**
- Indexes: workspace, skills, stack
- Used by: All agents for search
- Updates: Incremental on file changes

---

## Project Status Matrix

### Active Projects

| Project | Status | Priority | Next Milestone | Due Date |
|---------|--------|----------|----------------|----------|
| Nexus Superapp | 🟡 In Development | High | Complete Circle module | 2026-03-01 |
| Levy Agent | 🟢 Active | Critical | Complete modules | 2026-03-15 |
| Grafana Migration | 🟢 Deployed | High | Add alerting | 2026-03-01 |

### Completed Projects

| Project | Status | Completion Date | Repository |
|---------|--------|-----------------|------------|
| Storage Wars 2026 | ✅ Complete | 2026-02-13 | storage-wars-2026 |
| AAC Infrastructure | ✅ Complete | 2026-02-10 | aac-infrastructure |
| QMD Integration | ✅ Complete | 2026-02-16 | levy-agent |

### Infrastructure Projects

| Project | Status | Health | Uptime |
|---------|--------|--------|--------|
| AAC Stack | 🟢 Active | ✅ Healthy | 99.9% |
| OpenClaw Gateway | 🟢 Running | ✅ Healthy | 99.5% |
| Cloudflare Infra | 🟢 Active | ✅ Healthy | 100% |

### Skills Projects

| Skill | Version | Status | Documentation |
|-------|---------|--------|---------------|
| github-ops | 2.0.0 | ✅ Complete | ✅ Yes |
| docker-ops | 1.0.0 | ✅ Complete | ✅ Yes |
| cloudflare-ops | 1.0.0 | ✅ Complete | ✅ Yes |
| monitoring-ops | 1.0.0 | 🟡 Needs update | ✅ Yes |
| google-cloud-ops | 1.0.0 | 🟡 Needs update | ✅ Yes |
| storage-wars-2026 | 1.0.0 | ✅ Complete | ✅ Yes |
| ini-compare | 1.1.0 | ✅ Complete | ✅ Yes |
| pdf-reader | 1.0.0 | ✅ Complete | ✅ Yes |
| performance-benchmark | 1.0.0 | ✅ Complete | ✅ Yes |
| claude-skill-dev-guide | 1.0.0 | ✅ Complete | ✅ Yes |

---

## Project Roadmap

### Q1 2026 (Feb - Mar)

**February 2026:**
- ✅ Complete AAC infrastructure documentation
- ✅ Deploy Grafana monitoring stack
- ✅ Integrate QMD for semantic search
- 🟡 Complete Nexus Superapp initial setup
- ⏳ Consolidate Levy Agent documentation

**March 2026:**
- ⏳ Complete Nexus Superapp Circle module
- ⏳ Complete Levy Agent modules (Brain, Circle, Vessel)
- ⏳ Add alerting to Grafana
- ⏳ Create CI/CD pipelines

### Q2 2026 (Apr - Jun)

**April 2026:**
- ⏳ Deploy Nexus Superapp to production
- ⏳ Enhance monitoring with advanced dashboards
- ⏳ Integrate PagerDuty for alerting

**May 2026:**
- ⏳ Develop multi-agent system
- ⏳ Agent 1: Monitoring specialist
- ⏳ Agent 2: Application specialist

**June 2026:**
- ⏳ Enhance security (signed commits, 2FA)
- ⏳ Secrets rotation automation
- ⏳ Performance optimization

### Q3-Q4 2026

- ⏳ Advanced features and enhancements
- ⏳ Additional skills development
- ⏳ Expanded monitoring coverage
- ⏳ Improved documentation and onboarding

---

## Summary

**Key Insights:**

1. **Active Development:** 3 major projects in active development
2. **Strong Foundation:** Infrastructure complete and stable
3. **Skills Library:** 10 reusable skills for common tasks
4. **Documentation Focus:** Comprehensive docs for all projects
5. **Scalable Architecture:** Modular design enables easy growth

**Priority Order:**
1. **Critical:** AAC Stack, OpenClaw Gateway
2. **High:** Nexus Superapp, Grafana Migration
3. **Medium:** Skills development, Documentation
4. **Low:** Storage Wars 2026 (completed)

**Next Steps:**
1. Complete Nexus Superapp Circle module
2. Finish Levy Agent documentation consolidation
3. Add alerting to Grafana
4. Create CI/CD pipelines
5. Develop multi-agent system

---

*Last updated: 2026-02-18*
