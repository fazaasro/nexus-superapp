# AAC Infrastructure Overview

## Identity
- **Name:** Levy (Agent Faza)
- **Email:** agent-faza@gmail.com
- **GitHub:** Machine user account
- **Mission:** Level up Faza and Gaby through optimization of Finance, Mind, Social, and Health

## Network Architecture

### Private Access (Tailscale VPN)
- **VPS Tailscale IP:** 100.117.11.11
- **Laptop Access:** http://100.117.11.11:PORT
- Encrypted WireGuard tunnel

### Public Access (Cloudflare Tunnel)
- sit.yourdomain.com (staging)
- app.yourdomain.com (production)
- Public IP (95.111.237.115) exposes ONLY SSH (port 22)

## Core Services (via Caddy on Tailscale IP)

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| Portainer | 9000 | Docker management | http://100.117.11.11:9000 |
| n8n | 5678 | Workflow automation | http://100.117.11.11:5678 |
| Qdrant | 6333 | Vector DB / Memory | http://100.117.11.11:6333 |
| Code-Server | 8443 | VS Code in browser | http://100.117.11.11:8443 |
| Openclaw | 18789 | Agent gateway | http://100.117.11.11:18789 |

## File System Structure

```
/home/ai-dev/
├── stack/              # Infrastructure
│   ├── docker-compose.yml
│   ├── cloudflared/    # Tunnel credentials
│   └── .env           # Secrets (GH_TOKEN, TAILSCALE_KEY)
├── agents/            # Identity
│   ├── .ssh/          # GitHub deploy keys
│   ├── .gitconfig     # user.email = agent-faza@gmail.com
│   └── protocols/     # AGENT_PROTOCOL.md
└── swarm/             # Workflow
    ├── repos/         # Bare git repos
    └── ci-cd/         # Runner configs
```

## Development Flow

1. **Dev:** Work in ~/swarm/repos/<app>/dev-workspace/ using git worktrees
2. **SIT:** Push to develop branch → auto-deploys to sit.yourdomain.com
3. **Prod:** Merge to main → auto-deploys to app.yourdomain.com

## Security Layers (Critical)

1. **Docker:** Containers bind to 127.0.0.1 only
2. **Caddy:** Reverse proxy binds to Tailscale IP only (100.117.11.11)
3. **UFW Firewall:** Deny all incoming; allow SSH (22) + Tailscale only
4. **iptables:** DOCKER-USER chain drops leaked traffic

## CI/CD Pipeline

1. Agent codes in worktree → tests with Docker
2. Push to branch → GitHub Actions builds → pushes to GHCR
3. Webhook → n8n → Portainer redeploys container
4. Access via Cloudflare Tunnel rules

## NEVER Do

- Change Docker ports from 127.0.0.1:PORT to 0.0.0.0:PORT
- Change Caddy bind from 100.117.11.11 to : or 0.0.0.0
- Commit secrets to git
- Expose services directly to internet

## Comm Standards

- Conventional commits: feat:, fix:, docs:, refactor:, test:
- Always pull before pushing
