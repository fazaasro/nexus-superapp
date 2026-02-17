# Cloudflare Tunnel Fix Instructions

## Problem

**Error Message:**
```
ERR failed to serve incoming request error="Unauthorized: Invalid tunnel secret"
```

**Cause:** cloudflared service is configured with a hardcoded token that doesn't match your Cloudflare account.

## Solution

### Option 1: Use Existing Valid Configuration (RECOMMENDED) ✅

The current cloudflared service is already running with a valid token. The best approach is to update the configuration to use this valid token.

**Steps:**

1. **Stop current cloudflared service:**
   ```bash
   sudo systemctl stop cloudflared
   ```

2. **Update systemd service file to use credentials file:**
   ```bash
   sudo nano /etc/systemd/system/cloudflared.service
   ```

   Change the `ExecStart` line from:
   ```
   ExecStart=/usr/bin/cloudflared --no-autoupdate tunnel run --token <HARDCODED_TOKEN>
   ```

   To:
   ```
   ExecStart=/usr/bin/cloudflared --no-autoupdate tunnel --config /home/ai-dev/.config/cloudflared/config.yml --credentials-file /home/ai-dev/.config/cloudflared/credentials.json
   ```

3. **Update configuration files with valid token:**
   
   The current service is using this token:
   ```
   eyJhIjoiMTM2Nzk5MjU3OWM4NmJkMjMzMjgwYThjYTc5N2Q1MTUiLCJ0IjoiODY3OGZiMWEtZjM0ZS00ZTkwLWI5NjEtODE1MWZmZThkMDUxIiwicyI6Ik9DSG51cnJTVmxpZlpIem9JMmFCMldmZGtJQnJFUWkxMnk1cDFheVIrOE45ZDR6WC9MMncxOU5veUYvdmVHOGdtdUdoa3NWcnY0Sjk2MnVzdWhJS0NRPT0ifQ==
   ```

   Update `/home/ai-dev/.config/cloudflared/credentials.json`:
   ```json
   {
     "AccountTag": "8678fb1a-f34e-4e90-b961-8151ffe8d051",
     "TunnelID": "8678fb1a-f34e-4e90-b961-8151ffe8d051",
     "TunnelSecret": "eyJhIjoiMTM2Nzk5MjU3OWM4NmJkMjMzMjgwYThjYTc5N2Q1MTUiLCJ0IjoiODY3OGZiMWEtZjM0ZS00ZTkwLWI5NjEtODE1MWZmZThkMDUxIiwicyI6Ik9DSG51cnJTVmxpZlpIem9JMmFCMldmZGtJQnJFUWkxMnk1cDFheVIrOE45ZDR6WC9MMncxOU5veUYvdmVHOGdtdUdoa3NWcnY0Sjk2MnVzdWhJS0NRPT0ifQ==",
     "TunnelName": "monitor-grafana"
   }
   ```

4. **Reload systemd and restart service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart cloudflared
   sudo systemctl status cloudflared --no-pager
   ```

5. **Verify tunnel is running:**
   ```bash
   curl -I http://127.0.0.1:53681
   ```

### Option 2: Create New Tunnel via Cloudflare Dashboard 🔄

If Option 1 doesn't work, you'll need to create a new tunnel:

1. Go to https://dash.cloudflare.com
2. Navigate to Zero Trust → Access → Tunnels
3. Click "Create a tunnel"
4. Choose "Self-hosted"
5. Give it a name: `monitor-grafana`
6. Add hostname: `monitor-new.zazagaby.online`
7. Add service: `http://localhost:3000` (Grafana)
8. Save the tunnel and note the token

9. Update `/home/ai-dev/.config/cloudflared/credentials.json` with new token

10. Restart cloudflared service

## After Fix

Once the tunnel is working:

1. **Add DNS record** to Cloudflare DNS:
   ```
   Type: CNAME
   Name: monitor-new
   Target: 8678fb1a-f34e-4e90-b961-8151ffe8d051.cfargotunnel.com
   Proxy: No (or Orange)
   TTL: Auto
   ```

2. **Configure Access policy:**
   - Go to Zero Trust → Access → Applications
   - Create application: `monitor-grafana`
   - Add policy for ZG group (you and Gabriela)
   - Enable Email OTP authentication
   - Set session duration to 24h

3. **Test access:**
   ```bash
   curl -I https://monitor-new.zazagaby.online
   ```

4. **Login to Grafana:**
   ```
   URL: https://monitor-new.zazagaby.online
   Default credentials: admin / admin (first login, you'll be prompted to change)
   ```

## Files Created

- `/home/ai-dev/.config/cloudflared/config.yml` - Configuration file
- `/home/ai-dev/.config/cloudflared/credentials.json` - Credentials file
- `/home/ai-dev/.config/cloudflared/cloudflared-tunnel.service` - Systemd service file

## Current Status

- ✅ cloudflared service running
- ❌ Tunnel configuration mismatch (invalid token)
- ⏳ Requires manual service restart with updated configuration

## Quick Fix Commands

```bash
# 1. Update credentials with valid token
cat > /home/ai-dev/.config/cloudflared/credentials.json << 'EOF'
{
  "AccountTag": "8678fb1a-f34e-4e90-b961-8151ffe8d051",
  "TunnelID": "8678fb1a-f34e-4e90-b961-8151ffe8d051",
  "TunnelSecret": "eyJhIjoiMTM2Nzk5MjU3OWM4NmJkMjMzMjgwYThjYTc5N2Q1MTUiLCJ0IjoiODY3OGZiMWEtZjM0ZS00ZTkwLWI5NjEtODE1MWZmZThkMDUxIiwicyI6Ik9DSG51cnJTVmxpZlpIem9JMmFCMldmZGtJQnJFUWkxMnk1cDFheVIrOE45ZDR6WC9MMncxOU5veUYvdmVHOGdtdUdoa3NWcnY0Sjk2MnVzdWhJS0NRPT0ifQ==",
  "TunnelName": "monitor-grafana"
}
EOF

# 2. Stop and restart cloudflared
sudo systemctl stop cloudflared
sudo systemctl start cloudflared

# 3. Check status
sudo systemctl status cloudflared --no-pager
```
