# Levy's Integration Guide

**Last Updated:** 2026-02-10

---

## 📧 Gmail Account

**Email:** levynexus001@gmail.com  
**Purpose:** Levy's identity for API access and communications

### Access
- Direct API access (OAuth2)
- Google Workspace integration for Cloudflare SSO

### Uses
- OpenClaw notifications
- Email notifications from monitoring
- API authentication for Google services

---

## 🐙 GitHub Integration

**Account:** fazaasro (or agent-faza@gmail.com machine user)  
**Status:** ✅ Configured

### CLI Tool
```bash
gh auth status
# ✓ Logged in to github.com account fazaasro
# - Git operations protocol: https
# - Token: configured
```

### Available Repositories
- fazaasro/elegant-wedding-dress-rentals (private)
- fazaasro/guessroyale (private)
- fazaasro/django.nv (public)
- fazaasro/devsecops-repo (private)
- fazaasro/gcp-terraform (public)

### SSH Key
- Location: `~/.ssh/id_ed25519.pub`
- Status: ✅ Generated

### Git Configuration
```bash
git config --global user.name  # Agent Faza
git config --global user.email # agent-faza@gmail.com
```

### Common Commands
```bash
# List repos
gh repo list

# Create repo
gh repo create new-project --private

# Clone repo
gh repo clone owner/repo

# Push to GitHub
git push origin main

# Create PR
gh pr create --title "Fix bug" --body "Description"
```

---

## ☁️ Cloudflare Integration

**Account:** levynexus001@gmail.com  
**Zone:** zazagaby.online (cb7a80048171e671bd14e7ba2ead0623)  
**Status:** ✅ Fully Configured

### CLI Tool (cloudflared)
```bash
cloudflared --version
# cloudflared version 2026.2.0

# Tunnel management
cloudflared tunnel list
cloudflared tunnel create <name>
cloudflared tunnel route dns <tunnel-id> <subdomain>
```

### API Credentials
**API Key (Global):** `67685adc08f6a53ed01c79a718f67060e38a7`

### Current Tunnel
- **ID:** `8678fb1a-f34e-4e90-b961-8151ffe8d051`
- **Name:** levy-home-new
- **Status:** Active

### Protected Domains
| Domain | Service | Access |
|--------|---------|--------|
| admin.zazagaby.online | Portainer | Google SSO |
| n8n.zazagaby.online | n8n | Google SSO |
| code.zazagaby.online | Code-Server | Google SSO |
| qdrant.zazagaby.online | Qdrant | Google SSO |
| monitor.zazagaby.online | Overseer | Google SSO |
| agent.zazagaby.online | OpenClaw | Google SSO |

### Common Commands
```bash
# List tunnels
cloudflared tunnel list

# Show tunnel status
cloudflared tunnel info <tunnel-id>

# Create new route
cloudflared tunnel route dns <tunnel-id> app.zazagaby.online

# Update config
vim ~/.config/cloudflared/config.yml
```

---

## 🔧 Available CLI Tools

### Installed ✅
| Tool | Purpose |
|------|---------|
| `gh` | GitHub CLI |
| `cloudflared` | Cloudflare Tunnel CLI |
| `jq` | JSON processor |
| `docker` | Container management |
| `git` | Version control |

### Not Installed (Would need sudo)
| Tool | Purpose |
|------|---------|
| `fzf` | Fuzzy finder |
| `yq` | YAML processor |
| `mutt` | Email client |
| `msmtp` | SMTP client |

---

## 🤖 OpenClaw Integration

**Config:** `/home/ai-dev/.openclaw/openclaw.json`

### Models
| Model | Provider | Alias | Usage |
|-------|----------|-------|-------|
| zai/glm-4.7 | zai | GLM-4-Plus (Main) | Default |
| kimi-coding/k2p5 | kimi-coding | Kimi K2.5 (Backup) | Coding only |

### Gateway
- **Port:** 18789
- **Auth:** Token-based
- **Mode:** Local (127.0.0.1 only)

### Tools Available
All OpenClaw tools are available through the gateway API.

---

## 📊 Docker Integration

**Status:** ✅ Running

### Services
| Service | Container | Port |
|---------|-----------|------|
| Portainer | portainer | 9000 |
| n8n | n8n | 5678 |
| Qdrant | qdrant | 6333 |
| Code-Server | code-server | 8443 |
| Overseer | overseer | 8501 |

### Common Commands
```bash
# List containers
docker ps

# View logs
docker logs <container>

# Restart container
docker restart <container>

# Execute in container
docker exec -it <container> sh
```

---

## 🔐 Security Notes

1. **Never commit secrets** to git repositories
2. **API tokens** are stored in:
   - `/home/ai-dev/.openclaw/openclaw.json`
   - `/home/ai-dev/stack/.env`
   - `/etc/cloudflared/credentials.json`
3. **SSH keys** are in `~/.ssh/`
4. **Google SSO** protects all public services

---

## 🚀 Usage Patterns

### Development Workflow
```bash
# 1. Clone or create repo
gh repo clone fazaasro/project
cd project

# 2. Make changes
vim file.py

# 3. Commit and push
git add .
git commit -m "Add feature"
git push

# 4. Create PR (if needed)
gh pr create
```

### Deployment Workflow
```bash
# 1. Update docker-compose.yml
cd ~/stack
vim docker-compose.yml

# 2. Restart services
docker compose restart

# 3. Check status
docker ps
```

### Cloudflare Management
```bash
# 1. Update tunnel config
vim ~/.config/cloudflared/config.yml

# 2. Restart cloudflared
systemctl --user restart cloudflared

# 3. Test new route
curl https://new-service.zazagaby.online
```

---

## 📝 TODO: Future Integrations

1. **Gmail API** - Send/receive emails from CLI
2. **GitHub Actions** - Automated CI/CD
3. **Email Alerts** - Notifications from Overseer
4. **fzf** - Fuzzy finder for better CLI experience
5. **yq** - YAML processing for config files

---

*Integration status documented by Levy 🏗️*
