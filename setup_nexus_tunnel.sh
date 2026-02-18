#!/bin/bash

# Setup Nexus Tunnel Configuration Script
# This script configures the Cloudflare tunnel for Nexus Super App

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up Nexus tunnel configuration...${NC}"

# Backup existing configuration
sudo cp /etc/cloudflared/config.yml /etc/cloudflared/config.yml.backup.$(date +%Y%m%d_%H%M%S)

# Create new configuration with Nexus routes
sudo tee /etc/cloudflared/config.yml > /dev/null << 'EOF'
# Cloudflare Tunnel Configuration
# Account: levynexus001@gmail.com
# Tunnel: levy-home-new (8678fb1a-f34e-4e90-b961-8151ffe8d051)

tunnel: 8678fb1a-f34e-4e90-b961-8151ffe8d051
credentials-file: /etc/cloudflared/credentials.json

ingress:
  # Nexus Super App
  - hostname: nexus.zazagaby.online
    service: http://localhost:5173
  - hostname: nexus-api.zazagaby.online
    service: http://localhost:8000
  
  # Core Services
  - hostname: admin.zazagaby.online
    service: http://localhost:9000
  - hostname: n8n.zazagaby.online
    service: http://localhost:5678
  - hostname: code.zazagaby.online
    service: http://localhost:8443
  - hostname: qdrant.zazagaby.online
    service: http://localhost:6333
  - hostname: agent.zazagaby.online
    service: http://localhost:18789
  
  # Monitoring Stack
  - hostname: grafana.zazagaby.online
    service: http://localhost:3000
  - hostname: prometheus.zazagaby.online
    service: http://localhost:9090
  - hostname: node-exporter.zazagaby.online
    service: http://localhost:9100
  - hostname: blackbox.zazagaby.online
    service: http://localhost:9115
  
  # Legacy
  - hostname: monitor.zazagaby.online
    service: http://localhost:3000
  - hostname: dev.zazagaby.online
    service: http://localhost:9000
  - hostname: sit.zazagaby.online
    service: http://localhost:9000
  - hostname: app.zazagaby.online
    service: http://localhost:9000
  
  - service: http_status:404
EOF

# Restart cloudflared to apply changes
echo -e "${YELLOW}Restarting cloudflared...${NC}"
sudo systemctl restart cloudflared

# Wait for service to start
sleep 3

# Check status
if sudo systemctl is-active --quiet cloudflared; then
    echo -e "${GREEN}✓ Cloudflared restarted successfully${NC}"
else
    echo -e "${YELLOW}✗ Cloudflared failed to start. Check logs with: journalctl -u cloudflared${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Nexus tunnel configuration completed${NC}"
echo ""
echo "Nexus URLs configured:"
echo "  - Frontend: https://nexus.zazagaby.online"
echo "  - API: https://nexus-api.zazagaby.online"
echo ""
echo "Note: DNS records may take a few minutes to propagate."
