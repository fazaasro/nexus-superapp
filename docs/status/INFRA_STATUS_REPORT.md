# AAC Infrastructure Status Report

**Generated:** 2026-02-10 07:35 CET  
**Reporter:** Levy (Agent Faza)

---

## 🌐 Network Architecture

```
Internet → Cloudflare Access (Google SSO) → Cloudflare Tunnel → VPS → Services
```

### Domains & Access

| Domain | Service | Access |
|--------|---------|--------|
| admin.zazagaby.online | Portainer | Google SSO (faza, gaby) |
| n8n.zazagaby.online | n8n Workflows | Google SSO (faza, gaby) |
| code.zazagaby.online | Code-Server IDE | Google SSO (faza, gaby) |
| qdrant.zazagaby.online | Qdrant Vector DB | Google SSO (faza, gaby) |
| monitor.zazagaby.online | Overseer Dashboard | Google SSO (faza, gaby) |
| agent.zazagaby.online | OpenClaw Gateway | Google SSO (faza, gaby) |

---

## 🔧 Infrastructure Components

### Cloudflare (levynexus001@gmail.com)
- **Zone:** zazagaby.online (cb7a80048171e671bd14e7ba2ead0623)
- **Tunnel:** levy-home-new (8678fb1a-f34e-4e90-b961-8151ffe8d051) ✅ Active
- **Identity Provider:** Google OAuth ✅ Configured
- **Access Policy:** Allow fazaasro@gmail.com, gabriela.servitya@gmail.com

### VPS (95.111.237.115)
- **Tailscale IP:** 100.117.11.11
- **Docker Services:** 5 containers (portainer, n8n, qdrant, code-server, overseer)
- **Host Service:** OpenClaw on port 18789

### Docker Stack
```
portainer     → 127.0.0.1:9000  → admin.zazagaby.online
n8n           → 127.0.0.1:5678  → n8n.zazagaby.online
qdrant        → 127.0.0.1:6333  → qdrant.zazagaby.online
code-server   → 127.0.0.1:8443  → code.zazagaby.online
overseer      → 127.0.0.1:8501  → monitor.zazagaby.online
```

---

## 📊 Project Panopticon (Overseer)

### Status: Operational ✅

**Container:** stack-overseer (healthy)  
**Database:** SQLite with WAL mode (metrics.db)  
**Collector:** Running every 60s

### Dashboard Tabs

| Tab | Status | Features |
|-----|--------|----------|
| 🟢 Health | ✅ | Service status, running containers |
| 📈 Trends | ✅ | CPU/RAM charts, token burn, tool usage |
| 🛡️ Security | ✅ | SSH failures, Fail2Ban, event log |
| 🔌 Network | ✅ | Open ports scan, traffic metrics |
| 🤖 OpenClaw | ⚠️ | Placeholder (needs API endpoint) |

### Metrics Collected

| Category | Metrics |
|----------|---------|
| **Host** | CPU %, RAM %, Disk %, IO wait, Network I/O |
| **Apps** | HTTP status, latency (n8n, portainer, qdrant, code-server) |
| **Docker** | Running containers, restart counts |
| **Security** | SSH failures, banned IPs (Fail2Ban) |
| **Network** | Open ports: 22, 80, 443, 9000, 5678, 6333, 8443, 8501 |
| **Tokens** | API usage, costs (pending OpenClaw integration) |

---

## 🔐 Security

### Cloudflare Access
- **Authentication:** Google OAuth
- **Authorized Users:**
  - fazaasro@gmail.com (Faza)
  - gabriela.servitya@gmail.com (Gaby)
- **Session Duration:** 24 hours

### VPS Security
- **SSH:** Port 22 (key-based auth)
- **Firewall:** UFW (deny all, allow SSH + Tailscale)
- **Fail2Ban:** Monitoring (count tracked in dashboard)
- **SSH Failures:** 11,712+ detected (tracked)

---

## 📁 Key File Locations

```
/home/ai-dev/stack/
├── docker-compose.yml          # Service definitions
├── .env                       # Cloudflare credentials
└── cloudflared/              # (deprecated - using token)

/home/ai-dev/swarm/repos/overseer/
├── app.py                     # Streamlit dashboard
├── collector.py               # Metrics collector
├── db.py                      # Database handler
├── Dockerfile                 # Container build
└── requirements.txt           # Python deps

/etc/cloudflared/
├── config.yml                 # Tunnel config with routes
└── credentials.json           # Tunnel credentials

/etc/systemd/system/
└── cloudflared.service        # Systemd service

/home/ai-dev/.openclaw/workspace/memory/
├── 2026-02-08.md             # Birth of Levy
├── 2026-02-09.md             # (not created)
├── 2026-02-10.md             # Cloudflare migration
└── CLOUDFLARE_MIGRATION.md   # Migration log
```

---

## ✅ Working Features

1. **Zero-Trust Access** — All services behind Google SSO
2. **Real-time Monitoring** — 60s metric collection
3. **Service Health** — HTTP checks with latency tracking
4. **Docker Monitoring** — Running container status
5. **Security Auditing** — SSH failure detection
6. **Port Scanning** — Automated open port detection
7. **Fail2Ban Tracking** — Banned IP monitoring
8. **Web Dashboard** — Streamlit UI with 5 tabs

## ⚠️ Pending / Known Issues

1. **Container Table** — `KeyError: 'image'` needs fix verification
2. **OpenClaw Metrics** — Requires `/api/metrics` endpoint in OpenClaw
3. **Token Tracking** — Needs OpenClaw to log API usage to database
4. **Tool Usage** — Needs OpenClaw to track tool calls

---

## 🔑 Credentials Reference

**Cloudflare API (Global Key):**
- Email: levynexus001@gmail.com
- Key: `67685adc08f6a53ed01c79a718f67060e38a7`
- Account ID: `1367992579c86bd233280a8ca797d515`
- Zone ID: `cb7a80048171e671bd14e7ba2ead0623`

**GCP OAuth:**
- Client ID: `942455404349-8189jp0fctuf4jkablivhjr9066r7rpf.apps.googleusercontent.com`
- Status: Active in Cloudflare Access

**Tunnel:**
- ID: `8678fb1a-f34e-4e90-b961-8151ffe8d051`
- Token: In systemd service (not shown for security)

---

## 🚀 Next Actions (When Resuming)

1. Verify dashboard loads all 5 tabs without errors
2. Fix container image key issue if persists
3. Add `/api/metrics` endpoint to OpenClaw
4. Integrate token usage logging in OpenClaw
5. Add tool call tracking in OpenClaw

---

*Report generated by Levy 🏗️*  
*Autonomous Agent Cloud - Operational*
