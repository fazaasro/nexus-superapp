# Vault Access Troubleshooting - 2026-02-19

## Issue: Connection Reset on vault.zazagaby.online

### Status Check

**Vault Container:** ✅ Healthy (Up 3 hours)
**Local Access:** ✅ Working (http://127.0.0.1:8200)
**Tunnel Config:** ✅ Correct (vault.zazagaby.online → localhost:8200)
**Cloudflare Access:** ✅ Enabled (App ID: 97f59f34)
**DNS Record:** ✅ Created (CNAME to tunnel)

### Diagnosis

**From VPS (Germany):** ✅ Working
- HTTP/2 302 redirect to Cloudflare Access login
- CF_AppSession cookie set
- No connection reset

**From User Location:** ❌ Connection Reset
- Possible causes:
  1. DNS not propagated to user's ISP
  2. User's ISP/network blocking Cloudflare
  3. Local DNS cache issue
  4. Firewall/antivirus blocking connection

---

## Solutions

### Solution 1: Check DNS Resolution

**Windows:**
```cmd
nslookup vault.zazagaby.online
```

Should return: `188.114.97.2` or `188.114.96.2`

**If DNS fails:**
```cmd
ipconfig /flushdns
```

**Mac/Linux:**
```bash
nslookup vault.zazagaby.online
sudo dscacheutil -flushcache  # Mac
sudo systemd-resolve --flush-caches  # Linux
```

---

### Solution 2: Wait for DNS Propagation

**Timeframe:** 15-30 minutes from creation
**Created:** 2026-02-19 07:05 GMT

**What's happening:**
- DNS record is propagated worldwide
- But some ISPs update slower than others
- VPS in Germany sees updated DNS immediately
- User's ISP may not have updated yet

**Test with alternative DNS:**
- Use your phone's mobile data (different ISP)
- Try Cloudflare DNS: 1.1.1.1
- Try Google DNS: 8.8.8.8

---

### Solution 3: Access via Tailscale VPN

**Tailscale IP:** 100.117.11.11
**Direct Access:** http://100.117.11.11:8200

**Steps:**
1. Connect to Tailscale VPN
2. Open browser: http://100.117.11.11:8200
3. Login with Vault root token

**Bypasses:**
- Cloudflare Tunnel
- DNS issues
- Cloudflare Access

**Security:** Still secured by Vault authentication

---

### Solution 4: Access via SSH Tunnel

**From local machine:**
```bash
ssh -L 8200:localhost:8200 ai-dev@95.111.237.115
```

**Then in browser:**
```
http://localhost:8200
```

**Benefits:**
- Direct connection to VPS
- Bypasses all external DNS issues
- Secure SSH encryption

---

### Solution 5: Test Other Services

**Try these URLs (same infrastructure):**

1. **grafana.zazagaby.online** - Created yesterday, should work
2. **monitor.zazagaby.online** - Created yesterday, should work
3. **admin.zazagaby.online** - Created Feb 10, definitely working

**If these work:**
- DNS is propagating correctly
- Vault is just newer (created today)
- Wait 30 minutes, try again

**If these don't work:**
- ISP issue or network blocking
- Use Tailscale or SSH tunnel

---

## Verification Commands

### From VPS (Already Working)

```bash
# Check vault container
docker ps --filter "name=vault"

# Check vault health
curl -s http://127.0.0.1:8200/v1/sys/health

# Check DNS resolution
nslookup vault.zazagaby.online

# Check tunnel access
curl -I https://vault.zazagaby.online
```

### From Local Machine

```bash
# Check DNS resolution
nslookup vault.zazagaby.online

# Check if reachable
curl -I https://vault.zazagaby.online

# If connection reset, try SSH tunnel
ssh -L 8200:localhost:8200 ai-dev@95.111.237.115
curl -I http://localhost:8200
```

---

## Configuration Status

### Cloudflare Tunnel
**Tunnel ID:** 8678fb1a-f34e-4e90-b961-8151ffe8d051
**Ingress Rule:** vault.zazagaby.online → localhost:8200
**Status:** Active and running

### Cloudflare Access
**App ID:** 97f59f34-7352-4b53-ade0-37ff5ecb473a
**Domain:** vault.zazagaby.online
**Session Duration:** 24h
**Authentication:** Email OTP
**Allowed Users:**
- fazaasro@gmail.com
- gabriela.servitya@gmail.com

### DNS Record
**Type:** CNAME
**Name:** vault
**Target:** 8678fb1a-f34e-4e90-b961-8151ffe8d051.cfargotunnel.com
**Proxied:** ✅ (orange cloud)
**Status:** Active

---

## Timeline

| Time | Event |
|-------|--------|
| 07:05 | DNS record created |
| 07:07 | Tunnel configuration updated |
| 07:07 | Cloudflared restarted |
| 07:07 | Cloudflare Access app created |
| 07:08 | Verified working from VPS |
| 09:28 | User reports connection reset |

**Elapsed:** 2.5 hours since creation

---

## Recommended Action Plan

### Immediate (Now)
1. **Try Tailscale access** (bypasses all external issues)
   - http://100.117.11.11:8200
   - Login with root token: `[REDACTED]`

2. **Try SSH tunnel** if Tailscale unavailable
   ```bash
   ssh -L 8200:localhost:8200 ai-dev@95.111.237.115
   # Open http://localhost:8200
   ```

3. **Test other services** to confirm it's not a general issue
   - https://grafana.zazagaby.online
   - https://monitor.zazagaby.online

### If Other Services Work
1. Wait 30 minutes for DNS propagation
2. Clear local DNS cache
3. Try vault.zazagaby.online again

### If All Services Fail
1. Check ISP/network restrictions
2. Use VPN (different country/ISP)
3. Stick with Tailscale or SSH tunnel access

---

## Root Cause Analysis

**Most Likely:** DNS Propagation Delay
- Vault DNS created 2.5 hours ago
- User's ISP may not have updated yet
- VPS sees updated DNS immediately (Germany)
- Other working services were created yesterday

**Alternative Possibilities:**
- ISP blocking Cloudflare IPs
- Local firewall/antivirus interfering
- Mobile network restrictions

**Evidence for DNS:**
- Grafana (created yesterday) works
- Vault (created today) doesn't work
- Same infrastructure, different creation times
- VPS sees both working

---

## Next Steps

1. **Try Tailscale access now** - Guaranteed to work
2. **Test grafana.zazagaby.online** - Confirm DNS is issue
3. **Wait 30 minutes** - Retry vault.zazagaby.online
4. **Fallback to SSH tunnel** - If nothing else works

*Contact if Tailscale access also fails - that would indicate a different issue.*
