# TOOLS.md - AAC Infrastructure Reference

## Home Environment

**VPS:** Ubuntu 22.04 LTS  
**Domain:** zazagaby.online  
**Public IP:** 95.111.237.115  
**Tailscale IP:** 100.117.11.11  
**Location:** Germany (FRA/CDG)

## Network Architecture

```
Internet → Cloudflare Access (SSO) → Cloudflare Tunnel → VPS (localhost) → Docker
```

## Services

### Docker Services (localhost)
| Service | Port | Public URL | Purpose |
|---------|------|------------|---------|
| Portainer | 9000 | admin.zazagaby.online | Container management |
| n8n | 5678 | n8n.zazagaby.online | Workflow automation |
| Qdrant | 6333 | qdrant.zazagaby.online | Vector memory DB |
| Code-Server | 8443 | code.zazagaby.online | Browser IDE |
| Overseer | 8501 | monitor.zazagaby.online | Monitoring dashboard |
| Vault | 8200 | vault.zazagaby.online | Secrets management |

### Host Services
| Service | Port | Public URL | Purpose |
|---------|------|------------|---------|
| OpenClaw | 18789 | agent.zazagaby.online | Agent gateway (me) |
| Cloudflared | - | - | Tunnel connector (native) |

### Monitoring Services (localhost)
| Service | Port | Public URL | Purpose |
|---------|------|------------|---------|
| Grafana | 3000 | grafana.zazagaby.online | Monitoring dashboard |
| Prometheus | 9090 | prometheus.zazagaby.online | Metrics collector |
| Node Exporter | 9100 | node-exporter.zazagaby.online | System metrics |
| Blackbox Exporter | 9115 | blackbox.zazagaby.online | ICMP/TCP checks |

## Access Control

**Cloudflare Access Group:** ZG  
**Allowed Users:**
- fazaasro@gmail.com (Faza)
- gabriela.servitya@gmail.com (Gaby)

**Authentication:** Email OTP  
**Session Duration:** 24 hours

## File Locations

```
/home/ai-dev/
├── stack/                    # Infrastructure
│   ├── docker-compose.yml    # Core services
│   ├── .env                  # Secrets
│   └── cloudflared/          # Tunnel config
├── swarm/                    # Development workspace
│   └── repos/                # Git repositories
├── data/                     # Service data
│   ├── portainer/
│   ├── n8n/                  # SQLite DB
│   ├── qdrant/               # Vector store
│   └── code-server/
└── .openclaw/
    └── workspace/            # My home
        ├── SOUL.md
        ├── IDENTITY.md
        ├── USER.md
        └── memory/
```

## Docker Configuration

**Critical:** Services must bind to `127.0.0.1:PORT` so cloudflared can reach them:

```yaml
ports:
  - "127.0.0.1:9000:9000"  # ✅ Cloudflared can reach
expose:
  - "9000"                  # ❌ Only docker network
```

## Cloudflare Resources

**Account:** levynexus001@gmail.com (new)  
**Zone ID:** cb7a80048171e671bd14e7ba2ead0623  
**Tunnel ID:** 8678fb1a-f34e-4e90-b961-8151ffe8d051 (new)  
**Tunnel Name:** levy-home-new  
**Access Group ID:** a38eae36-eb86-4c98-9278-3fad2d253cfd

## Security Layers

1. **Docker:** Containers bind to 127.0.0.1
2. **Cloudflare Access:** SSO required for all subdomains
3. **Cloudflare Tunnel:** Encrypted outbound connection
4. **UFW Firewall:** Deny all except SSH + Tailscale

## Commands

```bash
# Check services
docker ps

# View cloudflared logs
journalctl -u cloudflared -f

# Test tunnel
curl https://admin.zazagaby.online

# Restart services
cd ~/stack && docker compose restart
```

## API Tokens

**CF_API_TOKEN:** `67685adc08f6a53ed01c79a718f67060e38a7`  
**GLM API Key:** `44ccf5decb22442e94be7e6271f84e47.eNJl2NFWKFOTaP8W`  
**Permissions:** DNS:Edit, Zone:Read, Access:*, Tunnel:Edit

---

## Helper Scripts (2026-02-10)

**Location:** `/home/ai-dev/.openclaw/workspace/scripts/`

Load all helpers:
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

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

## Accounts (2026-02-10)

| Service | Account | Purpose |
|---------|---------|---------|
| GitHub | fazaasro | Code repositories, CLI: `gh` |
| Cloudflare | levynexus001 | Domain, Tunnel, Access |
| Gmail | levynexus001 | SSO identity |
| OpenClaw | GLM-4.7 + Kimi K2.5 | AI models |

---

*Updated: 2026-02-10*
