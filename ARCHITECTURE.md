# ARCHITECTURE.md - System Architecture and Component Relationships

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Network Architecture](#network-architecture)
4. [Data Flow](#data-flow)
5. [Service Relationships](#service-relationships)
6. [Security Architecture](#security-architecture)
7. [Deployment Architecture](#deployment-architecture)

---

## System Overview

OpenClaw is a self-hosted autonomous AI agent platform running on a VPS with a distributed architecture that separates concerns across multiple services and layers.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OPENCLAW SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Gateway    │  │    QMD       │  │   Skills     │         │
│  │  (OpenClaw)  │  │  (Memory)    │  │  Repository  │         │
│  │   :18789     │  │  (Vector DB) │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                 │                 │                  │
│         └─────────────────┴─────────────────┘                  │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────┐         │
│  │              AGENT WORKSPACE                       │         │
│  │  - AGENTS.md (behavior)                          │         │
│  │  - MEMORY.md (long-term)                         │         │
│  │  - error-log.md (lessons learned)                │         │
│  │  - Daily logs (memory/YYYY-MM-DD.md)             │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────┐         │
│  │              AGENT MODULES                        │         │
│  │  - BAG (Document Analysis)                       │         │
│  │  - Brain (Decision Engine)                       │         │
│  │  - Circle (Social Memory)                        │         │
│  │  - Vessel (Sobriety Tracking)                    │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────┐         │
│  │           INFRASTRUCTURE SERVICES                 │         │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │         │
│  │  │ Portainer│ │    n8n   │ │  Qdrant  │         │         │
│  │  │  :9000   │ │  :5678   │ │  :6333   │         │         │
│  │  └──────────┘ └──────────┘ └──────────┘         │         │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │         │
│  │  │   Code   │ │  Overseer│ │  Grafana │         │         │
│  │  │  :8443   │ │  :8501   │ │  :3000   │         │         │
│  │  └──────────┘ └──────────┘ └──────────┘         │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────┐         │
│  │           CLOUDFLARE TUNNEL                       │         │
│  │  - Encrypted outbound connection                 │         │
│  │  - SSO authentication (Cloudflare Access)        │         │
│  │  - DNS routing (zazagaby.online)                 │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                     │
│                           ▼                                     │
│                    ┌──────────────┐                           │
│                    │  INTERNET    │                           │
│                    └──────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns:** Each service has a specific purpose
2. **Security by Default:** All services behind Cloudflare Access + Tunnel
3. **Local-First:** Services bind to localhost only
4. **Scalable Architecture:** Modular components can be added/removed
5. **Memory-Persistent:** Agent learns and remembers across sessions

---

## Component Architecture

### 1. OpenClaw Gateway

**Purpose:** Central gateway for agent communication and task execution

**Location:** Host service (not Docker)  
**Port:** 18789 (localhost)  
**Public URL:** agent.zazagaby.online

**Responsibilities:**
- Receive and route agent requests
- Manage agent sessions
- Execute commands via shell
- Coordinate with skills and modules
- Handle tool invocations (read, write, exec, browser, etc.)

**Configuration:**
- Environment variables in `~/.bashrc`
- Config file: `~/.openclaw/config/`
- Version: 2026.2.17 (as of 2026-02-18)

**Why Host Service?**
- Direct access to host system (no container isolation)
- Can run commands and manage Docker containers
- Better performance (no container overhead)

### 2. QMD (Query Memory Database)

**Purpose:** Semantic search across all agent knowledge

**Location:** Local installation (not Docker)  
**Database:** `~/.openclaw/workspace/qmd.db`

**Responsibilities:**
- Index multiple collections (workspace, skills, stack)
- Provide fast keyword search (BM25)
- Provide semantic search (Vector embeddings)
- Incremental updates for changed files

**Collections:**
- `workspace` - Agent workspace files
- `skills` - Skill documentation
- `stack` - Infrastructure code (aac-stack)

**Search Modes:**
- **BM25** (~240ms): Keyword-based, fast, 90% of searches
- **Vector** (~2s): Semantic understanding, finds related concepts
- **Hybrid** (~5s): Combines both, comprehensive search

**Why Local QMD?**
- No external dependencies
- Privacy (no cloud services)
- Fast incremental updates
- Offline capable

### 3. Skills Repository

**Purpose:** Reusable workflows and capabilities

**Location:** `~/.openclaw/workspace/skills/`  
**Count:** 10 skills (as of 2026-02-18)

**Skill Structure:**
```
skills/
├── README.md          # Skills registry
├── github-ops/        # GitHub operations
│   └── SKILL.md       # Skill documentation
├── docker-ops/        # Docker operations
│   └── SKILL.md
├── cloudflare-ops/    # Cloudflare operations
│   └── SKILL.md
├── monitoring-ops/    # Monitoring operations
│   └── SKILL.md
├── google-cloud-ops/  # GCP operations
│   └── SKILL.md
└── ...
```

**Skill Metadata:**
- `name`: Skill identifier
- `version`: Semantic versioning
- `description`: What the skill does
- `when_to_use`: When to invoke
- `when_not_to_use`: When NOT to invoke
- `tools_involved`: Tools used
- `workflows`: Available procedures
- `templates`: Reusable templates
- `guardrails`: Safety guidelines

**Available Skills:**
1. **github-ops** (v2.0.0) - Repository management, CI/CD
2. **docker-ops** (v1.0.0) - Docker container management
3. **cloudflare-ops** (v1.0.0) - Tunnel and DNS management
4. **monitoring-ops** (v1.0.0) - System health and metrics
5. **google-cloud-ops** (v1.0.0) - Gmail, Calendar, Drive integration
6. **storage-wars-2026** (v1.0.0) - Backend benchmarking
7. **ini-compare** (v1.1.0) - Configuration comparison
8. **pdf-reader** (v1.0.0) - PDF document analysis
9. **performance-benchmark** (v1.0.0) - Performance analysis
10. **claude-skill-dev-guide** (v1.0.0) - Skill development guide

### 4. Agent Memory System

**Purpose:** Persistent memory and learning across sessions

**Components:**

#### A. Daily Memory Files
**Location:** `memory/YYYY-MM-DD.md`  
**Purpose:** Raw logs of what happened  
**Format:** Free-form text with timestamps  
**Retention:** Indefinite

#### B. Long-term Memory (MEMORY.md)
**Location:** `MEMORY.md`  
**Purpose:** Curated wisdom and insights  
**Loading:** ONLY in main session (security)  
**Update Frequency:** Every 2-3 days during heartbeats

#### C. Error Log (error-log.md)
**Location:** `memory/error-log.md`  
**Purpose:** Immediate capture of failures and lessons  
**Loading:** ALWAYS in every session  
**Update Frequency:** IMMEDIATELY when something goes wrong

**Memory Architecture:**
```
┌─────────────────────────────────────────────┐
│              MEMORY SYSTEM                  │
├─────────────────────────────────────────────┤
│                                             │
│  Daily Files (memory/YYYY-MM-DD.md)         │
│  - Raw logs of every session                │
│  - Everything that happened                 │
│  - Written during session                    │
│                                             │
│  ────────────────────────────────────       │
│                                             │
│  MEMORY.md (Curated Wisdom)                 │
│  - Only important long-term info            │
│  - WHY decisions were made                  │
│  - Updated every few days                   │
│  - Loaded only in main session              │
│                                             │
│  ────────────────────────────────────       │
│                                             │
│  Error Log (memory/error-log.md)            │
│  - Immediate lessons learned                │
│  - Prevents repeating mistakes              │
│  - Loaded every session                     │
│  - Updated IMMEDIATELY on failure           │
│                                             │
└─────────────────────────────────────────────┘
```

### 5. Agent Modules

**Purpose:** Specialized capabilities for specific domains

**Location:** `modules/`  
**Count:** 4 modules (as of 2026-02-18)

#### A. BAG Module (Bank Account Garbage)
**Purpose:** Document analysis and extraction from financial documents  
**Features:**
- OCR-based document processing (EasyOCR, PaddleOCR)
- Text extraction and classification
- Receipt parsing (Indonesian receipts)
- API server for document analysis

**Technology:**
- Python 3.12+
- EasyOCR or PaddleOCR
- Flask/FastAPI for API server

**API Endpoint:** `/api/bag` (when server running)

#### B. Brain Module
**Purpose:** Decision engine and reasoning  
**Features:**
- Decision-making logic
- Task prioritization
- Resource allocation

**Status:** In development

#### C. Circle Module
**Purpose:** Social memory and relationship tracking  
**Features:**
- Track interactions with people
- Remember preferences and context
- Social relationship mapping

**Status:** In development

#### D. Vessel Module
**Purpose:** Sobriety tracking and recovery support  
**Features:**
- Sobriety tracker with relapse logging
- Milestone tracking
- Support resource recommendations

**Database:** SQLite (`database/vessel.db`)

### 6. Infrastructure Services

#### A. Portainer
**Purpose:** Docker container management UI  
**Port:** 9000 (localhost)  
**Public URL:** admin.zazagaby.online  
**Purpose:** Container management, deployment, monitoring

#### B. n8n
**Purpose:** Workflow automation  
**Port:** 5678 (localhost)  
**Public URL:** n8n.zazagaby.online  
**Purpose:** Visual workflow builder, automation, integrations

#### C. Qdrant
**Purpose:** Vector database for RAG (Retrieval Augmented Generation)  
**Port:** 6333 (localhost)  
**Public URL:** qdrant.zazagaby.online  
**Purpose:** Store and retrieve vector embeddings

#### D. Code Server
**Purpose:** Browser-based IDE  
**Port:** 8443 (localhost)  
**Public URL:** code.zazagaby.online  
**Purpose:** Edit code from anywhere in browser

#### E. Overseer
**Purpose:** Monitoring dashboard  
**Port:** 8501 (localhost)  
**Public URL:** monitor.zazagaby.online  
**Status:** Being migrated to Grafana

#### F. Grafana Stack (New)
**Purpose:** Modern monitoring solution  
**Components:**
- Prometheus (port 9090) - Time-series database
- Grafana (port 3000) - Visualization
- Node Exporter (port 9100) - Host metrics
- cAdvisor (port 8080) - Container metrics
- Blackbox Exporter (port 9115) - Health checks

**Status:** Deployed 2026-02-16

---

## Network Architecture

### Network Layers

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNET                              │
│                    (Public)                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CLOUDFLARE NETWORK                          │
│  ┌──────────────────────────────────────────────┐      │
│  │  Cloudflare Access (SSO)                    │      │
│  │  - Email OTP authentication                  │      │
│  │  - 24-hour session duration                 │      │
│  └──────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────┐      │
│  │  Cloudflare Tunnel                           │      │
│  │  - Encrypted outbound connection             │      │
│  │  - No open ports on VPS                      │      │
│  └──────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────┐      │
│  │  DNS Routing                                 │      │
│  │  - *.zazagaby.online → Tunnel               │      │
│  └──────────────────────────────────────────────┘      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 VPS FIREWALL (UFW)                      │
│  - Deny all incoming except SSH + Tailscale            │
│  - No public ports exposed                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                      VPS HOST                            │
│  ┌──────────────────────────────────────────────┐      │
│  │  Host Services (bind to 127.0.0.1)           │      │
│  │  - OpenClaw Gateway :18789                   │      │
│  │  - Cloudflared Tunnel Connector              │      │
│  └──────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────┐      │
│  │  Docker Network (localhost)                  │      │
│  │  - Portainer :9000                           │      │
│  │  - n8n :5678                                 │      │
│  │  - Qdrant :6333                              │      │
│  │  - Code Server :8443                         │      │
│  │  - Overseer :8501                            │      │
│  │  - Grafana :3000                             │      │
│  │  - Prometheus :9090                          │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Security Layers

1. **Cloudflare Access (SSO)**
   - Email OTP authentication
   - Allowed users: fazaasro@gmail.com, gabriela.servitya@gmail.com
   - Access Group: ZG
   - 24-hour session duration

2. **Cloudflare Tunnel**
   - Encrypted outbound connection (VPS → Cloudflare)
   - No open ports on VPS
   - Automatic TLS termination

3. **UFW Firewall**
   - Deny all incoming by default
   - Allow SSH (port 22)
   - Allow Tailscale (port 41641)
   - Block all other inbound traffic

4. **Localhost Binding**
   - All Docker services bind to `127.0.0.1`
   - Cloudflared reaches them via localhost
   - No direct internet access to services

### DNS Configuration

**Domain:** zazagaby.online  
**Zone ID:** cb7a80048171e671bd14e7ba2ead0623  
**Tunnel ID:** 8678fb1a-f34e-4e90-b961-8151ffe8d051

**Subdomains:**
| Subdomain | Service | Port |
|-----------|---------|------|
| agent | OpenClaw Gateway | 18789 |
| admin | Portainer | 9000 |
| n8n | n8n Automation | 5678 |
| qdrant | Vector Database | 6333 |
| code | Code Server | 8443 |
| monitor | Overseer/Grafana | 8501/3000 |

---

## Data Flow

### 1. Agent Request Flow

```
User (WhatsApp)
    │
    ▼
OpenClaw Gateway (:18789)
    │
    ├─► Load memory files (AGENTS.md, error-log.md, etc.)
    ├─► Search QMD for relevant info
    ├─► Invoke skills as needed
    ├─► Execute commands (via exec)
    ├─► Read/write files
    └─► Return response
```

### 2. Memory Write Flow

```
Agent Action
    │
    ├─► Write to memory/YYYY-MM-DD.md (daily log)
    │
    ├─► If error → Write to error-log.md (immediate)
    │
    └─► Periodically (heartbeat) → Update MEMORY.md (curated)
```

### 3. QMD Search Flow

```
Agent Query
    │
    ▼
QMD Search (BM25/Vector/Hybrid)
    │
    ├─► Search indexed collections
    │    ├─► workspace
    │    ├─► skills
    │    └─► stack
    │
    └─► Return ranked results
```

### 4. Skill Invocation Flow

```
User Request
    │
    ▼
Agent (reasoning)
    │
    ├─► Determine appropriate skill
    ├─► Load SKILL.md
    ├─► Follow documented workflow
    ├─► Execute tools (read, write, exec, etc.)
    └─► Return result
```

### 5. Monitoring Flow

```
Services (Docker)
    │
    ├─► cAdvisor (container metrics)
    ├─► Node Exporter (host metrics)
    └─► Blackbox Exporter (health checks)
         │
         ▼
    Prometheus (scrape metrics)
         │
         ▼
    Grafana (visualize)
```

---

## Service Relationships

### Dependency Graph

```
┌─────────────────────────────────────────────────────────┐
│                    DEPENDENCIES                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  OpenClaw Gateway                                       │
│    ├─► Depends on: QMD (for search)                    │
│    ├─► Depends on: Skills (for workflows)               │
│    ├─► Depends on: Memory files (for context)          │
│    └─► Manages: Docker services                        │
│                                                         │
│  QMD                                                    │
│    └─► Depends on: Workspace, skills, stack files     │
│                                                         │
│  Skills                                                 │
│    ├─► github-ops → GitHub API                         │
│    ├─► docker-ops → Docker daemon                       │
│    ├─► cloudflare-ops → Cloudflare API                 │
│    ├─► monitoring-ops → Grafana/Prometheus             │
│    └─► google-cloud-ops → Google APIs (via gog)         │
│                                                         │
│  Modules                                                │
│    ├─► BAG → EasyOCR/PaddleOCR                          │
│    ├─► Brain → (in development)                         │
│    ├─► Circle → (in development)                        │
│    └─► Vessel → SQLite database                         │
│                                                         │
│  Infrastructure Services                                │
│    ├─► Portainer → Docker daemon                        │
│    ├─► n8n → SQLite database                            │
│    ├─► Qdrant → Vector storage                         │
│    ├─► Grafana Stack → Prometheus                       │
│    └─► All services → Cloudflare Tunnel                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Communication Patterns

**Synchronous (Request-Response):**
- Gateway → Skills (skill invocation)
- Gateway → QMD (search)
- Gateway → Tools (read, write, exec)
- User → Gateway (WhatsApp messages)

**Asynchronous (Event-Driven):**
- Agent → Memory files (write)
- Agent → Error log (immediate logging)
- Cron jobs → Heartbeats
- Monitoring → Alerting

**Batch (Periodic):**
- Heartbeats → Multiple checks (email, calendar, etc.)
- QMD update → Index changed files
- Memory review → Distill daily files into MEMORY.md

---

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────┐
│              SECURITY LAYERS (Defense in Depth)         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: Cloudflare Access (SSO)                      │
│  - Email OTP authentication                            │
│  - Access Group: ZG                                    │
│  - 24-hour session duration                            │
│                                                         │
│  Layer 2: Cloudflare Tunnel                            │
│  - Encrypted outbound connection (TLS)                 │
│  - No open ports on VPS                                │
│  - Automatic certificate management                    │
│                                                         │
│  Layer 3: UFW Firewall                                  │
│  - Deny all inbound by default                         │
│  - Allow SSH (port 22) only                            │
│  - Allow Tailscale (port 41641) only                   │
│                                                         │
│  Layer 4: Localhost Binding                             │
│  - All services bind to 127.0.0.1                      │
│  - Cloudflared reaches via localhost                   │
│  - No direct internet access                           │
│                                                         │
│  Layer 5: Memory Protection                            │
│  - MEMORY.md only loaded in main session               │
│  - No personal context in shared contexts             │
│  - Secrets in environment variables                    │
│                                                         │
│  Layer 6: Git Security                                  │
│  - No secrets in code                                  │
│  - Private repositories                                │
│  - Signed commits (future)                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Access Control

**Allowed Users:**
- fazaasro@gmail.com (Faza) - Admin
- gabriela.servitya@gmail.com (Gaby) - User

**Authentication Method:**
- Email OTP (One-Time Password)
- 24-hour session duration
- Cloudflare Access Group: ZG

**Service Access:**
| Service | Access Level | Who Can Access |
|---------|--------------|----------------|
| OpenClaw Gateway | Full | Admin only |
| Portainer | Full | Admin only |
| n8n | Full | Admin + User |
| Qdrant | Read/Write | Services only |
| Code Server | Full | Admin only |
| Monitor | Read-only | Admin + User |

### Secrets Management

**Location:** Environment variables in `~/.bashrc` or Docker `.env`

**Never store in:**
- Git repositories
- Configuration files
- Documentation

**Secrets:**
```bash
# Cloudflare
CF_API_TOKEN=...
CF_ZONE_ID=...
CF_TUNNEL_ID=...

# GitHub
GH_TOKEN=...

# OpenClaw (if needed)
OPENCLAW_API_KEY=...

# Google Cloud (if needed)
GOOGLE_CREDENTIALS=...
```

---

## Deployment Architecture

### Deployment Layers

```
┌─────────────────────────────────────────────────────────┐
│              DEPLOYMENT ARCHITECTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────┐     │
│  │  GitHub Repositories (Source of Truth)       │     │
│  │  - levy-agent (workspace)                     │     │
│  │  - aac-stack (infrastructure)                │     │
│  │  - aac-infrastructure (docs)                  │     │
│  └──────────────────────────────────────────────┘     │
│                    │                                    │
│                    ▼                                    │
│  ┌──────────────────────────────────────────────┐     │
│  │  CI/CD Pipelines (GitHub Actions)            │     │
│  │  - Test → Lint → Build → Deploy             │     │
│  └──────────────────────────────────────────────┘     │
│                    │                                    │
│                    ▼                                    │
│  ┌──────────────────────────────────────────────┐     │
│  │  VPS (Ubuntu 22.04)                          │     │
│  │  - Host: vmi3072016                          │     │
│  │  - Location: Germany (FRA/CDG)               │     │
│  └──────────────────────────────────────────────┘     │
│                    │                                    │
│                    ▼                                    │
│  ┌──────────────────────────────────────────────┐     │
│  │  Docker Compose (Service Orchestration)      │     │
│  │  - aac-stack/docker-compose.yml             │     │
│  └──────────────────────────────────────────────┘     │
│                    │                                    │
│                    ▼                                    │
│  ┌──────────────────────────────────────────────┐     │
│  │  Services (Running)                          │     │
│  │  - Portainer, n8n, Qdrant, Code Server       │     │
│  │  - Grafana Stack (new)                       │     │
│  └──────────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Deployment Process

**New Service Deployment:**

1. **Development**
   - Write code locally
   - Test with test scripts
   - Document in SKILL.md

2. **Commit**
   ```bash
   git add .
   git commit -m "feat: add new service"
   git push
   ```

3. **CI/CD** (via GitHub Actions)
   - Run tests
   - Lint code
   - Build container (if applicable)
   - Deploy to VPS

4. **Deployment on VPS**
   ```bash
   cd ~/stack/aac-stack
   git pull
   docker compose up -d
   ```

5. **Monitoring**
   - Check service health via Grafana
   - Review logs via Portainer
   - Verify Cloudflare Tunnel route

### Rollback Strategy

**If deployment fails:**
1. Check logs: `docker logs <container>`
2. Rollback: `git revert` or `git checkout <previous-commit>`
3. Redeploy: `docker compose up -d --force-recreate`
4. Monitor: Watch Grafana for issues

---

## Architecture Evolution

### Completed Milestones

1. **Initial Setup** (2026-02-08)
   - VPS provisioned
   - Docker stack deployed
   - Cloudflare Tunnel configured
   - OpenClaw Gateway installed

2. **Skills Development** (2026-02-10 to 2026-02-15)
   - Created 10 skills
   - Documented workflows
   - Integrated with agent

3. **QMD Integration** (2026-02-16)
   - Installed QMD
   - Indexed collections
   - Configured search modes

4. **Grafana Migration** (2026-02-16)
   - Deployed Grafana stack
   - Configured Prometheus
   - Migrated from Overseer

### Future Plans

1. **Module Development** (Q2 2026)
   - Complete Brain module
   - Complete Circle module
   - Enhance Vessel module

2. **Advanced Monitoring** (Q2 2026)
   - Add alerting to Grafana
   - Integrate with PagerDuty
   - Custom dashboards

3. **Multi-Agent System** (Q3 2026)
   - Agent 1: Monitoring specialist
   - Agent 2: Application specialist
   - Agent coordination

4. **Enhanced Security** (Q3 2026)
   - Signed commits
   - 2FA for Git
   - Secrets rotation

---

## Summary

**Key Architectural Decisions:**

1. **Host Services for Gateway**
   - Direct access to system
   - Manage Docker containers
   - Better performance

2. **Docker for Infrastructure**
   - Easy deployment
   - Isolated services
   - Portainer management

3. **Cloudflare Tunnel + Access**
   - No open ports
   - SSO authentication
   - Automatic HTTPS

4. **QMD for Search**
   - Local and private
   - Semantic understanding
   - Fast incremental updates

5. **Skills for Reusability**
   - Consistent workflows
   - Documented procedures
   - Easy maintenance

6. **Memory for Learning**
   - Never repeat mistakes
   - Persistent context
   - Improves over time

**System Characteristics:**
- Secure (defense in depth)
- Scalable (modular components)
- Maintainable (documented workflows)
- Resilient (error logging + learning)
- Private (no external dependencies for core functions)

---

*Last updated: 2026-02-18*
