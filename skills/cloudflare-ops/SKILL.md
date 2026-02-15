---
name: cloudflare-ops
version: 1.0.0
description: |
  Cloudflare tunnel management, DNS configuration, and Access control for the AAC infrastructure.

when_to_use:
  - Creating new Cloudflare tunnels
  - Managing tunnel routes
  - Updating DNS records
  - Configuring Cloudflare Access
  - Tunnel troubleshooting

when_not_to_use:
  - Just listing tunnels (use 'cf-tunnels' helper)
  - Testing URLs (use 'cf-test' helper)
  - Non-tunnel network operations

tools_involved:
  - cloudflared-cli
  - cloudflare-api

network_policy: restricted
allowed_domains:
  - cloudflare.com
  - api.cloudflare.com
  - dash.cloudflare.com
  - 1.1.1.1.1
  - zazagaby.online

expected_artifacts:
  - Tunnel configurations
  - DNS route mappings
  - Access policies

success_criteria:
  - Tunnel created and running
  - DNS route added
  - Access policy configured
  - Service accessible via HTTPS

---

## Workflows

### create_tunnel

Creates a new Cloudflare tunnel.

**Parameters:**
- `name`: Tunnel name

**Steps:**
1. `cf-new $name`
2. Copy the tunnel ID from output
3. Create DNS route: `cf-route $tunnel_id $subdomain`
4. Update Cloudflare Access policy in dashboard

**Examples:**
```bash
# Create tunnel called "my-service"
create_tunnel my-service
# Output: Created tunnel: abc123-def456...
# Next: Run cf-route to add DNS
```

---

### add_route

Adds a DNS route to an existing tunnel.

**Parameters:**
- `tunnel_id`: Tunnel ID
- `subdomain`: Subdomain (e.g., myapp)
- `domain`: Domain (default: zazagaby.online)

**Steps:**
1. `cf-route $tunnel_id $subdomain $domain`
2. Verify DNS propagation
3. Test access: `cf-test https://$subdomain.$domain`

**Examples:**
```bash
# Add route to tunnel for new-service
add_route abc123-def456 new-service zazagaby.online
# Output: Route added: new-service.zazagaby.online
```

---

### list_tunnels

Lists all Cloudflare tunnels.

**Parameters:**
None

**Steps:**
1. `cf-tunnels`
2. Review tunnel status
3. Identify active/inactive tunnels

**Output:**
```
ID                                    Name                  Status      Connector
abc123-def456-ghi789-jkl012         levy-home-new         Active      vm-i3072016
```

**Examples:**
```bash
# List all tunnels
list_tunnels
```

---

### restart_tunnel

Restarts the Cloudflare tunnel service.

**Parameters:**
None

**Steps:**
1. `cf-restart`
2. Check status: `cf-tunnels`
3. Monitor logs if issues persist

**Examples:**
```bash
# Restart tunnel
restart_tunnel
# Output: Tunnel restarted
```

---

### test_url

Tests if a URL is accessible through Cloudflare.

**Parameters:**
- `url`: Full URL to test

**Steps:**
1. `cf-test $url`
2. Check response code
3. Verify SSO redirect (should be 302 to login)

**Examples:**
```bash
# test n8n endpoint
test_url https://n8n.zazagaby.online
# Output: HTTP/2 302 (redirecting to SSO)
```

---

### configure_access

Configures Cloudflare Access policy for a service.

**Parameters:**
- `service_name`: Display name
- `subdomain`: Subdomain
- `allowed_emails`: List of allowed emails

**Steps:**
1. Go to Cloudflare Access dashboard
2. Navigate to Zero Trust → Applications
3. Click "Add an application"
4. Configure:
   - Application name: $service_name
   - Session duration: 24h
   - Authentication: Google OAuth
   - Access policy: Allow specific emails
5. Copy Application ID

**Manual Steps:**
```
1. https://dash.cloudflare.com
2. Zero Trust → Applications → Add an application
3. Name: $service_name
4. Domain: https://$subdomain.zazagaby.online
5. Configure SSO
6. Add email policy
```

**Examples:**
```bash
# Configure Access for new service
configure_access "New Service" new-service fazaasro@gmail.com,gabriela.servitya@gmail.com
# Output: Access policy configured
```

---

## Templates

### tunnel_config

Standard tunnel configuration for config.yml:

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /etc/cloudflared/credentials.json

ingress:
  - hostname: subdomain.zazagaby.online
    service: http://localhost:8000
```

---

### access_policy_template

Cloudflare Access policy configuration:

```
Application: Service Name
Domain: subdomain.zazagaby.online
Authentication: Google OAuth
Allowed Emails:
  - fazaasro@gmail.com
  - gabriela.servitya@gmail.com

Session Duration: 24 hours
```

---

## Guardrails

1. **Never expose public SSH** — Always use Cloudflare Tunnel
2. **Use Google SSO** — Don't create additional auth systems
3. **Bind to 127.0.0.1** — Services must bind to localhost
4. **Rotate credentials** — Regularly update tunnel tokens
5. **Keep tunnel config synced** — Update ~/.config/cloudflared/config.yml

---

## Negative Examples

### When NOT to use this skill

- Just checking DNS status → Use external tools like `dig` or `nslookup`
- Testing connectivity → Use `cf-test` helper
- Non-Cloudflare DNS → Use domain registrar tools

### What to do instead

**Instead of:**
```
configure_access my-service
```

**Do:**
```
# First check if route exists
cf-tunnels

# If route exists, just update it
# (Manual update in dashboard)
```

---

## Artifact Locations

All artifacts created by this skill go to:
- `~/.config/cloudflared/config.yml` — Tunnel configuration
- `/etc/cloudflared/config.yml` — System tunnel config
- `/etc/cloudflared/credentials.json` — Tunnel credentials

---

## Current Configuration

**Account:** levynexus001@gmail.com
**Zone:** zazagaby.online
**Tunnel:** levy-home-new (8678fb1a-f34e-4e90-b961-8151ffe8d051)

**Active Routes:**
- admin.zazagaby.online → portainer:9000
- n8n.zazagaby.online → n8n:5678
- code.zazagaby.online → code-server:8443
- qdrant.zazagaby.online → qdrant:6333
- agent.zazagaby.online → openclaw:18789
- monitor.zazagaby.online → overseer:8501

---

## Version History

- 1.0.0 — Initial release with Cloudflare operations
