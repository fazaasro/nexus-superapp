#!/bin/bash
# Cloudflare helper functions for Levy

# List all tunnels
cf-tunnels() {
    cloudflared tunnel list
}

# Show tunnel info
cf-info() {
    local tunnel_id=$1
    
    if [ -z "$tunnel_id" ]; then
        echo "Usage: cf-info <tunnel-id>"
        return 1
    fi
    
    cloudflared tunnel info "$tunnel_id"
}

# Create DNS route for tunnel
cf-route() {
    local tunnel_id=$1
    local subdomain=$2
    local domain=${3:-"zazagaby.online"}
    
    if [ -z "$tunnel_id" ] || [ -z "$subdomain" ]; then
        echo "Usage: cf-route <tunnel-id> <subdomain> [domain]"
        return 1
    fi
    
    cloudflared tunnel route dns "$tunnel_id" "$subdomain.$domain"
}

# Create new tunnel
cf-new() {
    local name=$1
    
    if [ -z "$name" ]; then
        echo "Usage: cf-new <tunnel-name>"
        return 1
    fi
    
    local tunnel_id=$(cloudflared tunnel create "$name" | grep -oE '[a-f0-9-]{36}')
    echo "Created tunnel: $tunnel_id"
    echo "Run this to create DNS route:"
    echo "  cf-route $tunnel_id <subdomain>"
}

# Test tunnel
cf-test() {
    local url=$1
    
    if [ -z "$url" ]; then
        echo "Usage: cf-test <url>"
        return 1
    fi
    
    curl -I "$url" 2>&1 | head -5
}

# Restart cloudflared
cf-restart() {
    systemctl --user restart cloudflared
    sleep 2
    systemctl --user status cloudflared --no-pager
}

# View cloudflared logs
cf-logs() {
    journalctl --user -u cloudflared -f
}
