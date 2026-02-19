# Vault Secrets Registry - 2026-02-19

## Overview

All confidential information has been moved to HashiCorp Vault at vault.zazagaby.online

**Vault URL:** https://vault.zazagaby.online (SSO protected)
**Local Access:** http://127.0.0.1:8200

---

## Secret Paths

### 1. Cloudflare Account
**Path:** `secret/cloudflare-account`

| Key | Value |
|------|--------|
| email | levynexus001@gmail.com |
| account_id | 1367992579c86bd233280a8ca797d515 |
| zone_id | cb7a80048171e671bd14e7ba2ead0623 |
| domain | zazagaby.online |

---

### 2. Cloudflare API Token
**Path:** `secret/cloudflare-api-token`

| Key | Value |
|------|--------|
| api_token | 67685adc08f6a53ed01c79a718f67060e38a7 |
| tunnel_id | 8678fb1a-f34e-4e90-b961-8151ffe8d051 |
| zone_id | cb7a80048171e671bd14e7ba2ead0623 |

---

### 3. Cloudflare Tunnel
**Path:** `secret/cloudflare-tunnel`

| Key | Value |
|------|--------|
| tunnel_id | 8678fb1a-f34e-4e90-b961-8151ffe8d051 |
| tunnel_name | levy-home-new |
| tunnel_config_path | /home/ai-dev/.config/cloudflared/config.yml |

---

### 4. GLM API Key
**Path:** `secret/glm-api-key`

| Key | Value |
|------|--------|
| api_key | 44ccf5decb22442e94be7e6271f84e47.eNJl2NFWKFOTaP8W |

---

### 5. GitHub
**Path:** `secret/github`

| Key | Value |
|------|--------|
| faza_username | fazaasro |
| faza_email | fazaasro@gmail.com |
| levy_username | fazaasro |
| machine_user_email | agent-faza@gmail.com |

---

### 6. Server Info
**Path:** `secret/server-info`

| Key | Value |
|------|--------|
| vps_ip | 95.111.237.115 |
| tailscale_ip | 100.117.11.11 |
| ssh_user | ai-dev |
| ssh_port | 22 |

---

### 7. Service Passwords
**Path:** `secret/service-passwords`

| Key | Value |
|------|--------|
| code_server_password | changeme456 |
| portainer_user | admin |
| portainer_password | changeme456 |
| grafana_admin_user | admin |
| grafana_admin_password | admin |

---

### 8. Users
**Path:** `secret/users`

| Key | Value |
|------|--------|
| faza_email | fazaasro@gmail.com |
| gaby_email | gabriela.servitya@gmail.com |
| levy_email | agent-faza@gmail.com |

---

## How to Access Secrets

### Method 1: Vault CLI (Recommended)

```bash
# Set environment variables
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="<root-token>"

# List all secrets
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv list secret/

# Read a specific secret
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get secret/cloudflare-account

# Read a specific value
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get -field=api_token secret/cloudflare-api-token
```

### Method 2: Vault UI

1. Access: https://vault.zazagaby.online
2. Login with root token (from password manager)
3. Navigate to: secret → secret/data/
4. Click on any secret to view
5. Click "Download JSON" to export

### Method 3: GitHub Actions

```yaml
- name: Retrieve secret from Vault
  uses: hashicorp/vault-action@v2
  with:
    url: https://vault.zazagaby.online
    method: token
    token: ${{ secrets.VAULT_SECRET_ID }}
    roleId: ${{ secrets.VAULT_ROLE_ID }}
    secrets: |
      secret/data/cloudflare-api-token | CF_API_TOKEN ;
      secret/data/glm-api-key | GLM_API_KEY
```

### Method 4: AppRole (GitHub Actions)

```bash
# Login with AppRole
vault login -method=approle role_id="945989a3-d4ad-3a14-99ee-d6e0086d7c71" secret_id="41e44bae-a83d-2914-324d-c657b5df4dad"

# Read secrets (read-only policy)
vault kv get secret/cloudflare-account
vault kv get secret/glm-api-key
```

---

## Security Notes

### What's in Vault ✅
- Cloudflare API tokens and credentials
- GLM API key
- Service passwords
- Server connection info
- User information
- GitHub account details

### What's NOT in Vault (Secure Separately) 🔒
- **Vault Root Token:** Store in password manager (not in Vault itself)
- **Vault Unseal Keys:** Distribute to trusted team members (need 3 of 5)
- **GitHub SSH Keys:** Stored in ~/.ssh/ (add to GitHub manually)
- **Personal Access Tokens:** Generate and manage in GitHub UI

### Access Control
- **AppRole:** Read-only access for GitHub Actions
- **Root Token:** Full admin access (use sparingly)
- **SSO:** Cloudflare Access for UI (Email OTP, 24h sessions)

---

## Using Secrets in Scripts

### Example: Cloudflare API

```bash
# Retrieve API token
CF_API_TOKEN=$(docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get -field=api_token secret/cloudflare-api-token)

# Use in API call
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: levynexus001@gmail.com" \
  -H "X-Auth-Key: $CF_API_TOKEN"
```

### Example: Server Connection

```bash
# Retrieve server info
VPS_IP=$(docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get -field=vps_ip secret/server-info)
SSH_USER=$(docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get -field=ssh_user secret/server-info)

# Connect
ssh $SSH_USER@$VPS_IP
```

### Example: Python Script

```python
import requests

# Read from Vault (simplified - use hvac library in production)
response = requests.post(
    'http://127.0.0.1:8200/v1/secret/data/cloudflare-api-token',
    headers={'X-Vault-Token': VAULT_TOKEN}
)
data = response.json()['data']['data']
api_token = data['api_token']
```

---

## GitHub Integration

### Update Repository Secrets

Add these secrets to your GitHub repositories:

| Secret Name | Value Source |
|-------------|---------------|
| `VAULT_ADDR` | http://vault.zazagaby.online |
| `VAULT_ROLE_ID` | 945989a3-d4ad-3a14-99ee-d6e0086d7c71 |
| `VAULT_SECRET_ID` | 41e44bae-a83d-2914-324d-c657b5df4dad |

### Example Workflow

```yaml
name: Deploy with Vault Secrets
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Vault
        uses: hashicorp/vault-action@v2
        with:
          url: ${{ secrets.VAULT_ADDR }}
          method: approle
          roleId: ${{ secrets.VAULT_ROLE_ID }}
          secretId: ${{ secrets.VAULT_SECRET_ID }}

      - name: Deploy
        env:
          CF_API_TOKEN: ${{ env.CF_API_TOKEN }}
          GLM_API_KEY: ${{ env.GLM_API_KEY }}
        run: |
          # Deployment commands using secrets
          echo "Deploying with secured credentials..."
```

---

## Maintenance

### Rotate Secrets

**Recommended Interval:** Every 90 days

**Steps:**
1. Generate new secret (e.g., new API token)
2. Update Vault: `vault kv put secret/cloudflare-api-token api_token=<new-token>`
3. Test access with new secret
4. Revoke old secret in original service
5. Update any dependent applications

### Audit Access

**Check who accessed Vault:**
```bash
docker exec vault vault audit list
```

**View logs:**
```bash
journalctl -u vault -f
```

---

## Migration Checklist

### ✅ Completed
- [x] Cloudflare API token moved to Vault
- [x] GLM API key moved to Vault
- [x] Service passwords moved to Vault
- [x] Server info moved to Vault
- [x] User information moved to Vault
- [x] GitHub account info moved to Vault

### 🔄 In Progress
- [ ] Remove hardcoded secrets from `.env` files
- [ ] Update scripts to read from Vault
- [ ] Update GitHub Actions to use Vault
- [ ] Test all integrations with Vault secrets

### 📋 Next Steps
1. Update stack/.env to use Vault secrets
2. Update monitoring-ops to reference Vault
3. Update cloudflare-ops to reference Vault
4. Test all services after migration
5. Remove hardcoded secrets from documentation (or mark as "example")

---

## Quick Reference

**List all secrets:**
```bash
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv list secret/
```

**Get specific secret:**
```bash
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get secret/<name>
```

**Get specific value:**
```bash
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv get -field=<key> secret/<name>
```

**Update secret:**
```bash
docker exec -e VAULT_ADDR -e VAULT_TOKEN vault vault kv put secret/<name> key1=value1 key2=value2
```

---

*Registry Date: 2026-02-19*
*Vault Version: 1.21.3*
*Total Secrets: 8 paths, 30+ key-value pairs*
