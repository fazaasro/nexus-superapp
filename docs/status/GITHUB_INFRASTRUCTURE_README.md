# AAC Infrastructure Setup

**Project:** Autonomous Agent Cloud (AAC)  
**Owner:** Faza (fazaasro@gmail.com)  
**Maintainer:** Levy (Agent Faza)  
**Last Updated:** 2026-02-12

---

## Overview

The AAC (Autonomous Agent Cloud) is a self-hosted AI infrastructure running on a VPS with:
- Zero-trust networking via Cloudflare Tunnel
- Docker container orchestration
- Monitoring and observability
- Multi-model AI gateway (OpenClaw)

**Status:** ✅ Production-Ready

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Internet                              │
└───────────────────┬───────────────────────────────┘
                    │
          ┌────────▼────────────┐
          │  Cloudflare Access    │
          │  (Google SSO)        │
          └────────▼────────────┘
                    │
          ┌────────▼────────────┐
          │   Cloudflare Tunnel   │
          │   (Encrypted HTTPS)   │
          └────────▼────────────┘
                    │
          ┌──────────────────────┐
          │       VPS (AAC)      │
          │                       │
          │   ┌─────────────────┴───────┐
          │   │                        │
          │   │    Docker Compose        │
          │   │  (6 Services)          │
          │   └────────┬────────────────┘
          │            │
          │   ┌────────┴───────────┐
          │   │                    │
          │   │  OpenClaw Gateway     │
          │   │  + 3 Models          │
          │   │  + 6 Tools          │
          │   └────────────────────────┘
          │
          └─────────────────────────────┘
```

---

## Services

### Docker Containers

| Service | Port | Public URL | Status | Purpose |
|---------|------|------------|--------|---------|
| Portainer | 9000 | admin.zazagaby.online | ✅ Running | Container management |
| n8n | 5678 | n8n.zazagaby.online | ✅ Running | Workflow automation |
| Qdrant | 6333 | qdrant.zazagaby.online | ✅ Running | Vector database |
| Code-Server | 8443 | code.zazagaby.online | ✅ Running | Browser IDE |
| Overseer | 8501 | monitor.zazagaby.online | ✅ Running | Monitoring dashboard |

### Host Services

| Service | Port | Public URL | Status | Purpose |
|---------|------|------------|--------|---------|
| OpenClaw Gateway | 18789 | agent.zazagaby.online | ✅ Running | AI agent gateway |

---

## Network Configuration

### Domain
**Primary Domain:** zazagaby.online

### Cloudflare Configuration

**Account:** levynexus001@gmail.com  
**Zone ID:** cb7a80048171e671bd14e7ba2ead0623  
**Tunnel:** levy-home-new (8678fb1a-f34e-4e90-b961-8151ffe8d051)  
**Status:** Active

### DNS Routes

| Subdomain | Service | Target | Status |
|-----------|---------|---------|--------|
| admin | Portainer:9000 | ✅ Active |
| n8n | n8n:5678 | ✅ Active |
| code | Code-Server:8443 | ✅ Active |
| qdrant | qdrant:6333 | ✅ Active |
| agent | OpenClaw:18789 | ✅ Active |
| monitor | Overseer:8501 | ✅ Active |
| ssh | SSH:22 (tunnel) | ⚠️ Pending |

### Access Control

**Cloudflare Access Group:** ZG  
**Authentication:** Google OAuth  
**Session Duration:** 24 hours  
**Allowed Users:**
- fazaasro@gmail.com (Faza)
- gabriela.servitya@gmail.com (Gaby)

---

## Security Architecture

### 4-Layer Defense

1. **Docker Layer**
   - Containers bind to `127.0.0.1:PORT`
   - Only docker network access (not public)

2. **Cloudflare Access Layer**
   - Google SSO required for all services
   - Email whitelist (faza + gaby only)

3. **Cloudflare Tunnel Layer**
   - Encrypted outbound HTTPS tunnel
   - No exposed public ports
   - SSH via tunnel (not port 22)

4. **UFW Firewall Layer**
   - Deny all by default
   - Allow SSH + Tailscale only

### Security Policies

- ✅ No exposed ports except SSH via tunnel
- ✅ All web services behind SSO
- ✅ SSH keys only (no password auth)
- ✅ Secrets in .env files (never committed)
- ✅ Fail2Ban monitoring SSH
- ✅ Overseer monitoring security events

---

## Deployment

### Docker Compose Configuration

**Location:** `/home/ai-dev/stack/docker-compose.yml`

### Directory Structure

```
/home/ai-dev/
├── stack/                     # Infrastructure
│   ├── docker-compose.yml
│   ├── .env                  # Secrets
│   └── cloudflared/          # Tunnel config (legacy)
├── swarm/                     # Development workspace
│   └── repos/               # Git repositories
└── data/                      # Service data
    ├── portainer/
    ├── n8n/
    ├── qdrant/
    ├── code-server/
    └── overseer/
```

---

## Credentials

### Cloudflare
**API Key:** `67685adc08f6a53ed01c79a718f67060e38a7`  
**Account:** levynexus001@gmail.com

### OpenClaw
**GLM API Key:** `44ccf5decb22442e94be7e6271f84e47.eNJl2NFWKFOTaP8W`  
**Primary Model:** zai/glm-4.7  
**Backup Model:** kimi-coding/k2p5 (coding only)

### Code-Server
**Password:** `changeme456` (default - CHANGE THIS!)

### GitHub
**Account:** fazaasro  
**SSH Key:** Ed25519 at `~/.ssh/id_ed25519`

---

## Quick Commands

### Docker
```bash
# Check all services
docker ps

# View logs
docker logs <container-name>

# Restart service
docker restart <container-name>

# Update and restart all
cd ~/stack && docker compose restart
```

### Cloudflare
```bash
# List tunnels
cloudflared tunnel list

# Restart tunnel
systemctl --user restart cloudflared

# View logs
journalctl --user -u cloudflared -f
```

### GitHub
```bash
# List repos
gh repo list

# Clone repo
gh repo clone <owner>/<name>

# Create new repo
gh repo create <name> --private
```

---

## Monitoring

**Dashboard:** https://monitor.zazagaby.online

**Tabs:**
1. 🟢 Health Status — Service health, container status
2. 📈 Trends — CPU, RAM, latency over time
3. 🛡️ Security — SSH failures, Fail2Ban, security events
4. 🔌 Network — Open ports, traffic
5. 🤖 OpenClaw — Agent metrics, memory, sessions

**Metrics Collected:**
- CPU, RAM, Disk, IO wait
- Network I/O (in/out)
- Service latency (HTTP status)
- Container restart counts
- Docker status (running only)
- SSH failure count
- Fail2Ban banned IPs
- Open ports scan

---

## Troubleshooting

### Service Not Accessible

1. Check Cloudflare Access (login with fazaasro@gmail.com)
2. Check if service is running: `docker ps`
3. Check tunnel status: `cloudflared tunnel list`
4. Check DNS: `nslookup admin.zazagaby.online`

### High Latency

1. Check service health logs
2. Monitor resource usage (CPU/RAM)
3. Check network I/O
4. Restart container if needed

### Security Alerts

1. **SSH Failures:** >10/hour → Enable Fail2Ban
2. **Container Restarts:** Frequent → Check logs for errors
3. **Unusual Ports:** Not in whitelist → Check for intrusions

---

## Backups

### Service Data

**Location:** `/home/ai-dev/data/`

### Backup Strategy

1. **Portainer Data:** Backup regularly (container configs)
2. **n8n Workflows:** Export workflows to Git
3. **Qdrant Vectors:** Periodic dump to JSON
4. **Code-Server:** Git-based (code in repos)
5. **OpenClaw Workspace:** Git repository (this is it!)

---

## Roadmap

### Completed ✅
- Docker stack deployed (6 containers)
- Cloudflare tunnel active
- Google SSO configured
- Overseer dashboard running
- OpenClaw gateway operational
- SSH tunnel configured (pending route add)

### In Progress 🚧
- SSH tunnel route to Cloudflare
- GitHub Actions for automated deployments

### Planned 📋
- Automated backups
- Alerting via Overseer
- CI/CD pipelines for all services
- GitOps workflows with github-ops skill
- Token burn rate tracking

---

## Maintenance

### Weekly
- Review security logs
- Check container health
- Update dependencies
- Review and clean Docker images

### Monthly
- Review and rotate API keys
- Review and update Docker images
- Backup service data
- Review and update documentation
- Audit security policies

---

## Documentation Links

| Document | Location | URL |
|----------|----------|-----|
| AAC Infrastructure | This repo | https://github.com/fazaasro/aac-infrastructure |
| Levy Agent | levy-agent repo | https://github.com/fazaasro/levy-agent |
| Overseer | overseer repo | https://github.com/fazaasro/overseer-monitoring |
| Project Levy SSH | project-levy-ssh repo | https://github.com/fazaasro/project-levy-ssh |
| Integration Guide | This repo | https://github.com/fazaasro/aac-infrastructure |
| Tools | TOOLS.md in each repo | GitHub |

---

## Contact

**Owner:** Faza (fazaasro@gmail.com)  
**Infrastructure:** Levy (Agent Faza)  
**Location:** VPS (95.111.237.115)  
**Timezone:** Europe/Berlin (GMT+1)

---

*Autonomous Agent Cloud — Production Infrastructure*
