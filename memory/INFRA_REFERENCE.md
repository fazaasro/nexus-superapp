# AAC Infrastructure Reference

Quick reference for the Autonomous Agent Cloud infrastructure.

## Domain & Network

- **Domain:** zazagaby.online
- **Public IP:** 95.111.237.115
- **Tailscale IP:** 100.117.11.11
- **VPS Location:** Germany

## Services

### Public Access (Cloudflare SSO)
| Service | URL | Local Port |
|---------|-----|------------|
| Portainer | admin.zazagaby.online | localhost:9000 |
| n8n | n8n.zazagaby.online | localhost:5678 |
| Code-Server | code.zazagaby.online | localhost:8443 |
| Qdrant | qdrant.zazagaby.online | localhost:6333 |
| OpenClaw (me) | agent.zazagaby.online | localhost:18789 |

### VPN Access (Tailscale)
All services available at: `http://100.117.11.11:PORT`

## Security

- **Cloudflare Access:** Email OTP required
- **Allowed Users:** fazaasro@gmail.com, gabriela.servitya@gmail.com
- **Session:** 24 hours
- **Tunnel ID:** b10b5897-1726-4245-b1c2-f2db56377016

## File Locations

```
/home/ai-dev/stack/         # Infrastructure code
/home/ai-dev/swarm/          # Development workspace
/home/ai-dev/data/           # Service data (persisted)
/etc/cloudflared/            # Tunnel config (native)
```

## Commands

```bash
# Restart all services
cd ~/stack && docker compose restart

# View logs
journalctl -u cloudflared -f
docker logs -f n8n

# Test services
curl http://localhost:9000/api/status
curl https://admin.zazagaby.online
```

## Key Lessons

1. Docker services must bind to `127.0.0.1` not just `expose`
2. Cloudflared runs NATIVE (systemd), not in Docker
3. API token can't modify tunnel routes — use dashboard
4. DNS must be CNAME to `<tunnel-id>.cfargotunnel.com`
5. Always ask before infrastructure changes

---

*Reference card for quick lookups. Full docs in TOOLS.md*
