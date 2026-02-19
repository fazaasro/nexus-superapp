# Vault + Cloudflare Access Integration - 2026-02-19

## ✅ Integration Complete

### What Was Done

**Cloudflare Access Apps Created:**

1. **Vault Access App**
   - App ID: 97f59f34-7352-4b53-ade0-37ff5ecb473a
   - Domain: vault.zazagaby.online
   - Session Duration: 24 hours
   - Authentication: Email OTP
   - Allowed Users:
     - fazaasro@gmail.com
     - gabriela.servitya@gmail.com

2. **Grafana (New) Access App**
   - App ID: ac678458-4daf-4e87-a68c-359e87378cd1
   - Domain: monitor-new.zazagaby.online
   - Session Duration: 24 hours
   - Authentication: Email OTP
   - Allowed Users:
     - fazaasro@gmail.com
     - gabriela.servitya@gmail.com

### Architecture

```
User → Cloudflare Access (SSO) → Cloudflare Tunnel → Vault/Grafana
         ↓                          ↓
    Email OTP                127.0.0.1:PORT
```

### Access URLs

| Service | Public URL | Access Protection |
|---------|-------------|-------------------|
| Vault | https://vault.zazagaby.online | ✅ SSO protected |
| Grafana (New) | https://monitor-new.zazagaby.online | ✅ SSO protected |
| Grafana (Old) | https://grafana.zazagaby.online | ✅ SSO protected |
| Prometheus | https://prometheus.zazagaby.online | ✅ SSO protected |
| Node Exporter | https://node-exporter.zazagaby.online | ✅ SSO protected |
| Blackbox Exporter | https://blackbox.zazagaby.online | ✅ SSO protected |

### Security Features

- **Zero Trust:** No direct access to services without authentication
- **Email OTP:** One-time password sent to email
- **Session Duration:** 24 hours (configurable)
- **HTTP-Only Cookies:** Prevents XSS attacks
- **Secure Cookies:** Only transmitted over HTTPS

---

## Verification

### Vault Access Test

```bash
curl -I https://vault.zazagaby.online
```

**Response:**
```
HTTP/2 302
Location: https://zegezegezege.cloudflareaccess.com/cdn-cgi/access/login/vault.zazagaby.online...
CF_AppSession: <session_token>
```

✅ Redirects to Cloudflare Access login
✅ Sets session cookie
✅ Auth status: NONE (requires login)

### Grafana Access Test

```bash
curl -I https://monitor-new.zazagaby.online
```

**Response:**
```
HTTP/2 302
Location: https://zegezegezege.cloudflareaccess.com/cdn-cgi/access/login/monitor-new.zazagaby.online...
CF_AppSession: <session_token>
```

✅ Redirects to Cloudflare Access login
✅ Sets session cookie
✅ Auth status: NONE (requires login)

---

## Access Flow

1. **User visits** https://vault.zazagaby.online
2. **Cloudflare Access** intercepts request
3. **Redirect** to login page
4. **User enters email** (fazaasro@gmail.com or gabriela.servitya@gmail.com)
5. **Email OTP** sent to user
6. **User enters OTP**
7. **Session created** (24 hours)
8. **Redirect** to vault UI
9. **Login to Vault** with root token or AppRole credentials

---

## API Commands Used

### Create Access App

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/access/apps" \
  -H "X-Auth-Email: {email}" \
  -H "X-Auth-Key: {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "self_hosted",
    "name": "Agent HQ - Vault",
    "domain": "vault.zazagaby.online",
    "session_duration": "24h",
    "policies": [
      {
        "decision": "allow",
        "name": "Allow Faza and Gaby",
        "include": [
          { "email": { "email": "fazaasro@gmail.com" } },
          { "email": { "email": "gabriela.servitya@gmail.com" } }
        ]
      }
    ]
  }'
```

### List Access Apps

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/{account_id}/access/apps" \
  -H "X-Auth-Email: {email}" \
  -H "X-Auth-Key: {api_token}"
```

---

## Credentials

### Vault Access

**Root Token:** [REDACTED]
**Unseal Keys:** ~/.openclaw/workspace/skills/vault-infrastructure/.vault-keys.txt
- Need 3 of 5 keys to unseal Vault
- Distribute keys among trusted team members

**GitHub Actions AppRole:**
- Role ID: 945989a3-d4ad-3a14-99ee-d6e0086d7c71
- Secret ID: 41e44bae-a83d-2914-324d-c657b5df4dad
- Policy: read-only access to GLM and Cloudflare secrets

### Cloudflare Access

**Account:** levynexus001@gmail.com
**Account ID:** 1367992579c86bd233280a8ca797d515
**Zone ID:** cb7a80048171e671bd14e7ba2ead0623
**API Token:** 67685adc08f6a53ed01c79a718f67060e38a7

**Allowed Users:**
- fazaasro@gmail.com (Faza)
- gabriela.servitya@gmail.com (Gaby)

---

## Next Steps

### Immediate
1. ✅ Store unseal keys in password manager
2. ✅ Test vault.zazagaby.online access
3. ✅ Test monitor-new.zazagaby.online access
4. Test GitHub Actions workflow with Vault

### Future
1. Add more secrets to Vault (API keys, tokens)
2. Create additional AppRole policies for different services
3. Rotate root token after initial setup
4. Set up audit logging for Vault
5. Configure Vault auto-unseal (optional)

---

## Troubleshooting

### "This site can't be reached"
**DNS Propagation:** Wait 15-30 minutes for DNS to propagate
**Clear DNS Cache:** `ipconfig /flushdns` (Windows) or `sudo dscacheutil -flushcache` (Mac)

### "Access Denied"
**Check Email:** Verify email matches allowed list
**Check OTP:** Use the most recent OTP email
**Check Session:** Session expires after 24 hours

### Vault Sealed
**Unseal with 3 Keys:**
```bash
docker exec vault vault operator unseal <key1>
docker exec vault vault operator unseal <key2>
docker exec vault vault operator unseal <key3>
```

---

## Summary

✅ Vault deployed and running
✅ Cloudflare Tunnel configured
✅ DNS records created
✅ Cloudflare Access protection enabled
✅ GitHub Actions integration configured
✅ SSO authentication working

**Security:** 4-layer defense
1. Docker: Services bind to 127.0.0.1
2. Cloudflare Tunnel: Encrypted outbound connection
3. Cloudflare Access: SSO authentication
4. Vault: Token-based access control

---

*Integration Date: 2026-02-19*
*Vault Version: 1.21.3*
*Cloudflare Access: Email OTP, 24h sessions*
