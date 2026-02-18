# DEPLOYMENT.md - Setup and Configuration Guide

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Infrastructure Setup](#infrastructure-setup)
3. [OpenClaw Gateway Setup](#openclaw-gateway-setup)
4. [Skills Installation](#skills-installation)
5. [QMD Configuration](#qmd-configuration)
6. [Environment Variables](#environment-variables)
7. [Services Deployment](#services-deployment)
8. [Monitoring Setup](#monitoring-setup)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

---

## Prerequisites

### System Requirements

**VPS Specifications:**
- OS: Ubuntu 22.04 LTS (or newer)
- RAM: Minimum 4GB (8GB recommended)
- CPU: 2 cores minimum (4 cores recommended)
- Storage: 50GB minimum (100GB recommended)
- Network: Public IP with SSH access

**Software Requirements:**
- Docker 20.10+
- Docker Compose 2.0+
- Git 2.30+
- Node.js 18+ (for OpenClaw Gateway)
- Python 3.10+ (for modules)
- Bun 1.0+ (for QMD)

**Domain Requirements:**
- Domain name (e.g., zazagaby.online)
- Cloudflare account (Free tier works)
- Ability to configure DNS records

### Accounts Needed

1. **GitHub Account** - For code repositories and CI/CD
2. **Cloudflare Account** - For tunnel, DNS, and access control
3. **Google Cloud Account** (Optional) - For GCP integrations

---

## Infrastructure Setup

### Step 1: VPS Provisioning

1. **Create VPS:**
   - Choose a provider (DigitalOcean, Linode, AWS, etc.)
   - Select Ubuntu 22.04 LTS
   - Configure size (4GB RAM, 2 CPUs minimum)
   - Set up SSH keys

2. **Connect to VPS:**
   ```bash
   ssh ai-dev@your-vps-ip
   ```

3. **Update System:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Step 2: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in for group changes to take effect
```

**Verify installation:**
```bash
docker --version
docker compose version
```

### Step 3: Configure Firewall

```bash
# Install UFW
sudo apt install ufw -y

# Default deny all incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow 22/tcp

# Allow Tailscale (if using)
sudo ufw allow 41641/udp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Step 4: Install Node.js and Bun

```bash
# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
npm --version

# Install Bun
curl -fsSL https://bun.sh/install | bash

# Add Bun to PATH (add to ~/.bashrc)
echo 'export BUN_INSTALL="$HOME/.bun"' >> ~/.bashrc
echo 'export PATH="$BUN_INSTALL/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
bun --version
```

### Step 5: Install Python

```bash
# Install Python 3.10+
sudo apt install python3 python3-pip python3-venv -y

# Verify
python3 --version
pip3 --version
```

---

## OpenClaw Gateway Setup

### Step 1: Install OpenClaw Gateway

```bash
# Download and install OpenClaw
curl -fsSL https://get.openclaw.dev/install.sh | bash

# Verify installation
openclaw --version
```

### Step 2: Configure Gateway

```bash
# Create OpenClaw directory
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
mkdir -p ~/.openclaw/config

# Set environment variables (add to ~/.bashrc)
cat >> ~/.bashrc << 'EOF'

# OpenClaw Environment
export OPENCLAW_HOME=/home/ai-dev/.openclaw
export OPENCLAW_WORKSPACE=/home/ai-dev/.openclaw/workspace
export OPENCLAW_CONFIG=/home/ai-dev/.openclaw/config

# OpenClaw Gateway
export OPENCLAW_GATEWAY_HOST=127.0.0.1
export OPENCLAW_GATEWAY_PORT=18789
EOF

# Reload .bashrc
source ~/.bashrc
```

### Step 3: Start Gateway

```bash
# Start OpenClaw Gateway
openclaw gateway start

# Check status
openclaw gateway status

# View logs
journalctl -u openclaw-gateway -f
```

### Step 4: Configure as System Service

```bash
# Create systemd service file
sudo tee /etc/systemd/system/openclaw-gateway.service > /dev/null <<EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=ai-dev
WorkingDirectory=/home/ai-dev/.openclaw
ExecStart=/usr/local/bin/openclaw gateway start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway

# Check status
sudo systemctl status openclaw-gateway
```

---

## Skills Installation

### Step 1: Clone Skills Repository

```bash
# Navigate to workspace
cd ~/.openclaw/workspace

# Initialize git repository
git init
git remote add origin https://github.com/fazaasro/levy-agent.git

# Pull skills
git pull origin main
```

### Step 2: Verify Skills

```bash
# List all skills
ls -la ~/.openclaw/workspace/skills/

# Verify each skill has SKILL.md
for skill in ~/.openclaw/workspace/skills/*/; do
  echo "=== $(basename "$skill") ==="
  ls "$skill/SKILL.md" 2>/dev/null && echo "✅ OK" || echo "❌ Missing"
done
```

### Step 3: Test Skills

Test each skill to ensure it works correctly:

```bash
# Test github-ops
cd ~/.openclaw/workspace/skills/github-ops
# Follow SKILL.md instructions

# Test docker-ops
cd ~/.openclaw/workspace/skills/docker-ops
# Follow SKILL.md instructions

# Test cloudflare-ops
cd ~/.openclaw/workspace/skills/cloudflare-ops
# Follow SKILL.md instructions
```

---

## QMD Configuration

### Step 1: Install QMD

```bash
# Install QMD via Bun
cd ~/.openclaw/workspace
bun add qmd

# Or install globally
bun install -g qmd

# Install tsx (required by QMD)
bun add tsx
```

### Step 2: Create QMD Configuration

Create `~/.openclaw/workspace/qmd.config.ts`:

```typescript
export default {
  collections: [
    {
      name: 'workspace',
      paths: ['/home/ai-dev/.openclaw/workspace'],
      exclude: ['node_modules', '.git', 'venv', '__pycache__', 'paddle_env*'],
    },
    {
      name: 'skills',
      paths: ['/home/ai-dev/.openclaw/workspace/skills'],
      exclude: ['node_modules', '.git', 'venv', '__pycache__'],
    },
    {
      name: 'stack',
      paths: ['/home/ai-dev/stack/aac-stack'],
      exclude: ['node_modules', '.git', 'venv', '__pycache__'],
    },
  ],
};
```

### Step 3: Build QMD Index

```bash
# Build index (first time takes ~7 minutes)
qmd build

# Update index (incremental, fast)
qmd update

# Test search
qmd search "docker compose"
qmd vsearch "how to deploy"
qmd query
```

---

## Environment Variables

### Required Environment Variables

Create `~/.openclaw/workspace/.env`:

```bash
# ===========================================
# OpenClaw Environment Variables
# ===========================================

# OpenClaw Configuration
export OPENCLAW_HOME=/home/ai-dev/.openclaw
export OPENCLAW_WORKSPACE=/home/ai-dev/.openclaw/workspace
export OPENCLAW_CONFIG=/home/ai-dev/.openclaw/config

# OpenClaw Gateway
export OPENCLAW_GATEWAY_HOST=127.0.0.1
export OPENCLAW_GATEWAY_PORT=18789

# ===========================================
# Cloudflare Configuration
# ===========================================

# Cloudflare API Token (Permissions: DNS:Edit, Zone:Read, Access:*, Tunnel:Edit)
export CF_API_TOKEN=your_cloudflare_api_token_here

# Cloudflare Zone ID
export CF_ZONE_ID=your_zone_id_here

# Cloudflare Tunnel ID
export CF_TUNNEL_ID=your_tunnel_id_here

# Cloudflare Account Email
export CF_ACCOUNT_EMAIL=your_email@example.com

# ===========================================
# GitHub Configuration
# ===========================================

# GitHub Personal Access Token
export GH_TOKEN=your_github_token_here

# GitHub Username
export GH_USERNAME=your_github_username

# ===========================================
# Google Cloud Configuration (Optional)
# ===========================================

# Google Cloud Credentials
export GOOGLE_CREDENTIALS=/path/to/credentials.json

# Google Project ID
export GOOGLE_PROJECT_ID=your_project_id

# ===========================================
# Optional: OCR Configuration
# ===========================================

# EasyOCR Model Directory
export EASYOCR_MODEL_DIR=/path/to/easyocr/models

# PaddleOCR Model Directory
export PADDLEOCR_MODEL_DIR=/path/to/paddleocr/models
```

### Load Environment Variables

Add to `~/.bashrc`:

```bash
# Load OpenClaw environment
if [ -f ~/.openclaw/workspace/.env ]; then
  source ~/.openclaw/workspace/.env
fi
```

Reload shell:

```bash
source ~/.bashrc
```

---

## Services Deployment

### Step 1: Clone AAC Stack

```bash
# Create stack directory
mkdir -p ~/stack
cd ~/stack

# Clone AAC Stack
git clone https://github.com/fazaasro/aac-stack.git
cd aac-stack
```

### Step 2: Configure Docker Compose

Review and customize `docker-compose.yml`:

```yaml
version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce:latest
    ports:
      - "127.0.0.1:9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "127.0.0.1:5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password_here
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  code-server:
    image: codercom/code-server:latest
    ports:
      - "127.0.0.1:8443:8443"
    volumes:
      - code_server_data:/home/coder
    environment:
      - PASSWORD=your_password_here
    restart: unless-stopped

volumes:
  portainer_data:
  n8n_data:
  qdrant_data:
  code_server_data:
```

### Step 3: Deploy Services

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Step 4: Verify Services

```bash
# Test Portainer
curl http://127.0.0.1:9000

# Test n8n
curl http://127.0.0.1:5678

# Test Qdrant
curl http://127.0.0.1:6333/health

# Test Code Server
curl http://127.0.0.1:8443
```

---

## Monitoring Setup

### Step 1: Deploy Grafana Stack

Create `docker-compose.monitoring.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "127.0.0.1:9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "127.0.0.1:3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=your_password_here
    restart: unless-stopped

  node_exporter:
    image: prom/node-exporter:latest
    ports:
      - "127.0.0.1:9100:9100"
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/host'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker:/var/lib/docker:ro
    restart: unless-stopped

  blackbox_exporter:
    image: prom/blackbox-exporter:latest
    ports:
      - "127.0.0.1:9115:9115"
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

### Step 2: Configure Prometheus

Create `prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node_exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'blackbox_exporter'
    static_configs:
      - targets: ['blackbox_exporter:9115']
```

### Step 3: Deploy Monitoring

```bash
# Start monitoring stack
docker compose -f docker-compose.monitoring.yml up -d

# Check status
docker compose -f docker-compose.monitoring.yml ps
```

### Step 4: Access Grafana

1. Open browser to `http://your-vps-ip:3000`
2. Login with admin/your_password_here
3. Add Prometheus datasource (http://prometheus:9090)
4. Import dashboards

---

## Cloudflare Tunnel Setup

### Step 1: Create Cloudflare Account

1. Sign up at https://dash.cloudflare.com
2. Add your domain (e.g., zazagaby.online)
3. Update domain nameservers to Cloudflare's nameservers

### Step 2: Install Cloudflared

```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify
cloudflared --version
```

### Step 3: Create Tunnel

```bash
# Authenticate with Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create levy-home

# Note the tunnel ID (e.g., 8678fb1a-f34e-4e90-b961-8151ffe8d051)
```

### Step 4: Configure Tunnel

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: 8678fb1a-f34e-4e90-b961-8151ffe8d051
credentials-file: /home/ai-dev/.cloudflared/8678fb1a-f34e-4e90-b961-8151ffe8d051.json

ingress:
  - hostname: agent.zazagaby.online
    service: http://localhost:18789
  - hostname: admin.zazagaby.online
    service: http://localhost:9000
  - hostname: n8n.zazagaby.online
    service: http://localhost:5678
  - hostname: qdrant.zazagaby.online
    service: http://localhost:6333
  - hostname: code.zazagaby.online
    service: http://localhost:8443
  - hostname: monitor.zazagaby.online
    service: http://localhost:3000
  - service: http_status:404
```

### Step 5: Start Tunnel

```bash
# Start tunnel in foreground (testing)
cloudflared tunnel run

# Or start as system service
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

### Step 6: Configure DNS Routes

```bash
# Create DNS routes
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 agent.zazagaby.online
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 admin.zazagaby.online
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 n8n.zazagaby.online
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 qdrant.zazagaby.online
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 code.zazagaby.online
cloudflared tunnel route dns 8678fb1a-f34e-4e90-b961-8151ffe8d051 monitor.zazagaby.online
```

### Step 7: Configure Access (SSO)

1. Go to Cloudflare Dashboard → Zero Trust → Access
2. Create Access Group (e.g., "ZG")
3. Add allowed users (emails)
4. Create Access Policy for each service:
   - Action: Allow
   - Group: ZG
   - Authentication: One-Time Pin (email)

---

## Troubleshooting

### Common Issues

**Issue: Docker containers won't start**

```bash
# Check Docker status
sudo systemctl status docker

# Check Docker logs
sudo journalctl -u docker -n 50

# Restart Docker
sudo systemctl restart docker
```

**Issue: Cloudflare tunnel not connecting**

```bash
# Check cloudflared status
sudo systemctl status cloudflared

# View logs
sudo journalctl -u cloudflared -f

# Test tunnel
cloudflared tunnel info 8678fb1a-f34e-4e90-b961-8151ffe8d051
```

**Issue: OpenClaw gateway not responding**

```bash
# Check gateway status
openclaw gateway status

# View logs
journalctl -u openclaw-gateway -f

# Restart gateway
openclaw gateway restart
```

**Issue: Services not accessible**

```bash
# Check if service is running
docker ps

# Check service logs
docker logs <container_name>

# Test local access
curl http://localhost:9000
```

**Issue: QMD search not working**

```bash
# Rebuild index
qmd build

# Check config
cat ~/.openclaw/workspace/qmd.config.ts

# Test search
qmd search "test"
```

### Diagnostic Commands

```bash
# System info
uname -a
df -h
free -m
top

# Docker info
docker version
docker info
docker ps -a

# Network info
netstat -tlnp
ss -tlnp

# Services
sudo systemctl status docker
sudo systemctl status cloudflared
sudo systemctl status openclaw-gateway
```

---

## Maintenance

### Daily Tasks

```bash
# Check service health
docker ps

# Check disk space
df -h

# Check system load
uptime
```

### Weekly Tasks

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker compose pull
docker compose -f docker-compose.monitoring.yml pull

# Restart services
docker compose up -d
docker compose -f docker-compose.monitoring.yml up -d
```

### Monthly Tasks

```bash
# Clean Docker resources
docker system prune -a

# Rotate logs
sudo journalctl --rotate
sudo journalctl --vacuum-time=30d

# Backup important data
# (Create backup scripts as needed)
```

### Backup Strategy

**What to Backup:**
- `~/.openclaw/workspace/` - Agent workspace
- `~/.openclaw/config/` - OpenClaw config
- `~/stack/aac-stack/` - Infrastructure code
- Docker volumes (Portainer, n8n, Qdrant)

**Backup Commands:**

```bash
# Backup workspace
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw

# Backup Docker volumes
docker run --rm -v portainer_data:/data -v $(pwd):/backup ubuntu tar czf /backup/portainer-backup.tar.gz /data
docker run --rm -v n8n_data:/data -v $(pwd):/backup ubuntu tar czf /backup/n8n-backup.tar.gz /data
docker run --rm -v qdrant_data:/data -v $(pwd):/backup ubuntu tar czf /backup/qdrant-backup.tar.gz /data
```

---

## Summary

**Deployment Checklist:**

- [ ] VPS provisioned and updated
- [ ] Docker and Docker Compose installed
- [ ] Firewall configured
- [ ] Node.js and Bun installed
- [ ] Python installed
- [ ] OpenClaw Gateway installed and running
- [ ] Skills cloned and verified
- [ ] QMD installed and configured
- [ ] Environment variables configured
- [ ] AAC Stack services deployed
- [ ] Grafana monitoring deployed
- [ ] Cloudflare Tunnel configured
- [ ] DNS routes created
- [ ] Access policies configured
- [ ] All services tested

**Next Steps:**

1. Test all services via their public URLs
2. Configure monitoring alerts
3. Set up automated backups
4. Create CI/CD pipelines
5. Document any customizations

---

*Last updated: 2026-02-18*
