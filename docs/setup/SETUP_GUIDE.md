# Integration Setup Guide

**For:** Levy (Agent Faza)  
**Date:** 2026-02-10

---

## ✅ Completed Integrations

### 1. GitHub ✅
- **Account:** fazaasro
- **CLI Tool:** `gh` installed and configured
- **SSH Key:** Generated at `~/.ssh/id_ed25519.pub`
- **Git Config:** User: Agent Faza, Email: agent-faza@gmail.com
- **Status:** Ready to use

### 2. Cloudflare ✅
- **Account:** levynexus001@gmail.com
- **Zone:** zazagaby.online
- **CLI Tool:** `cloudflared` installed (v2026.2.0)
- **Tunnel:** levy-home-new (active)
- **Access:** Google SSO configured
- **Status:** Fully operational

### 3. Docker ✅
- **Status:** Running
- **Services:** 5 containers (portainer, n8n, qdrant, code-server, overseer)
- **CLI Tool:** Available

### 4. OpenClaw ✅
- **Models:** GLM-4.7 (main) + Kimi K2.5 (backup)
- **Gateway:** Port 18789
- **Status:** Running

### 5. Gmail 📧
- **Account:** levynexus001@gmail.com
- **Status:** Configured for Google SSO
- **Note:** CLI tools need sudo (not available)

---

## 🎯 Helper Scripts Created

All scripts are in `/home/ai-dev/.openclaw/workspace/scripts/`

### `helpers.sh` - Main Loader
Load all helpers:
```bash
source ~/.openclaw/workspace/scripts/helpers.sh
levy-help
```

### GitHub Helpers (`gh-helpers.sh`)
| Command | Description |
|---------|-------------|
| `gh-check` | Check auth status |
| `gh-repos` | List repositories |
| `gh-new <name>` | Create new repository |
| `gh-pr` | Create pull request |
| `gh-issues` | List issues |
| `gh-issue <title>` | Create issue |

### Cloudflare Helpers (`cf-helpers.sh`)
| Command | Description |
|---------|-------------|
| `cf-tunnels` | List all tunnels |
| `cf-info <id>` | Show tunnel info |
| `cf-route <id> <subdomain>` | Create DNS route |
| `cf-new <name>` | Create new tunnel |
| `cf-test <url>` | Test URL |
| `cf-restart` | Restart cloudflared |
| `cf-logs` | View logs |

### Docker Helpers (`docker-helpers.sh`)
| Command | Description |
|---------|-------------|
| `docker-running` | List running containers |
| `docker-all` | List all containers |
| `docker-log <container>` | View logs |
| `docker-follow <container>` | Follow logs |
| `docker-restart <container>` | Restart container |
| `docker-exec <container>` | Execute in container |
| `docker-stats` | Show stats |
| `docker-cleanup` | Remove unused resources |
| `docker-check` | Check AAC services |
| `docker-restart-all` | Restart all services |

---

## 🚀 Quick Start

### 1. Load Helpers (add to `~/.bashrc`)
```bash
echo 'source ~/.openclaw/workspace/scripts/helpers.sh' >> ~/.bashrc
source ~/.bashrc
```

### 2. Test GitHub Integration
```bash
gh-check
gh-repos
```

### 3. Test Docker Integration
```bash
docker-check
```

### 4. Test Cloudflare Integration
```bash
cf-test https://admin.zazagaby.online
```

---

## 📧 Gmail Integration Notes

**Status:** Configured for SSO, no CLI access (requires sudo)

### Current Uses:
- Cloudflare Access SSO authentication
- API integration available

### Future Options (requires sudo):
```bash
# Install email clients
sudo apt install mutt msmtp

# Configure msmtp for sending
vim ~/.msmtprc

# Configure mutt for reading
vim ~/.muttrc
```

---

## 🔐 Security Best Practices

1. **Never commit secrets** to GitHub
2. **Use environment variables** for sensitive data
3. **Rotate API keys** regularly
4. **Review SSH key access** periodically
5. **Enable 2FA** on all accounts

---

## 📊 Current Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Levy (Agent Faza)                      │
│                    🏗️ Autonomous Agent Cloud              │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐        ┌───▼────┐        ┌────▼────┐
   │  GitHub  │        │Cloudflare│       │  Gmail  │
   │   gh CLI │        │ cloudflare│       │  SSO    │
   └──────────┘        └──────────┘        └─────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                   ┌────────▼────────┐
                   │  VPS (AAC Stack) │
                   ├─────────────────┤
                   │  • Docker (5)    │
                   │  • OpenClaw     │
                   │  • Overseer     │
                   │  • Tailscale    │
                   └─────────────────┘
```

---

## 📝 Documentation Files

| File | Description |
|------|-------------|
| `INTEGRATION_GUIDE.md` | Complete integration reference |
| `INFRA_STATUS_REPORT.md` | Infrastructure status |
| `TOOL_GUIDES/gh-guide.md` | GitHub CLI guide |
| `TOOL_GUIDES/cf-guide.md` | Cloudflare guide |
| `TOOL_GUIDES/docker-guide.md` | Docker guide |

---

## 🔧 Common Workflows

### Deploy New Service
```bash
# 1. Create Docker container
cd ~/stack
vim docker-compose.yml

# 2. Add cloudflared route
cf-route 8678fb1a-f34e-4e90-b961-8151ffe8d051 new-service

# 3. Add Access policy in Cloudflare dashboard

# 4. Test
cf-test https://new-service.zazagaby.online
```

### Create GitHub Repo
```bash
gh-new new-project
cd new-project
# ... work ...
git add .
git commit -m "Initial commit"
git push
```

### Monitor Services
```bash
# Check all services
docker-check

# View logs
docker-log overseer

# Restart if needed
docker-restart n8n
```

---

## ✅ Verification Checklist

- [x] GitHub CLI configured
- [x] SSH keys generated
- [x] Git config set up
- [x] Cloudflare tunnel active
- [x] Google SSO working
- [x] Docker services running
- [x] Helper scripts created
- [x] Documentation written
- [ ] Gmail CLI tools (requires sudo)
- [ ] fzf/yq installed (requires sudo)

---

## 🎓 Next Steps

1. **Add helpers to `~/.bashrc`** for auto-loading
2. **Set up GitHub Actions** for CI/CD
3. **Configure email alerts** from Overseer
4. **Install fzf/yq** when sudo available
5. **Set up automated backups**

---

*Setup complete! Levy is ready for maximum productivity. 🏗️*
