# 2026-02-10 — Project Levy (Remote AI Gateway)

## Task
Enable secure, remote execution of AI CLI tools (claude-code) through Cloudflare Zero Trust tunnel. Support macOS, Linux, and native Windows (PowerShell).

---

## Completed ✅

### 1. Workspace Setup
- Directory: `/home/ai-dev/levy_workspace`
- Permissions: ai-dev:ai-dev
- Status: Ready

### 2. Toolchain Verified
| Tool | Version | Status |
|-------|---------|--------|
| claude-code | Latest | ✅ Installed |
| git | 2.43.0 | ✅ Available |
| node | v22.22.0 | ✅ Available |

### 3. SSH Keys
- Type: Ed25519
- Private: `~/.ssh/id_ed25519`
- Public: `~/.ssh/id_ed25519.pub`

### 4. Documentation Created
All files in `/home/ai-dev/levy_workspace/`:
- `README_CONNECT.md` — Complete client connection guide
- `SSH_CONFIG_UPDATE_NEEDED.md` — Server update instructions
- `SETUP_STATUS.md` — Quick status reference

---

## Pending ⚠️

### SSH Tunnel Rule (Requires Sudo)

**File:** `/etc/cloudflared/config.yml`

**Add this rule before catch-all:**
```yaml
# SSH Gateway (for Remote AI Gateway)
- hostname: ssh.zazagaby.online
  service: ssh://localhost:22
```

**Prepared config:** `/tmp/cloudflared_config_new.yml`

**Command to apply:**
```bash
sudo cp /tmp/cloudflared_config_new.yml /etc/cloudflared/config.yml
sudo systemctl restart cloudflared
```

---

## Access Methods

### VS Code Remote SSH (Preferred)
- Works on all OS
- No file transfer latency
- Feels like local dev

### File Sync (Fallback)
- macOS/Linux: rsync
- Windows Native: scp (built-in)

---

## Client Configuration

### macOS / Linux
```ssh
Host levy
  HostName ssh.zazagaby.online
  User ai-dev
  IdentityFile ~/.ssh/id_ed25519
  ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
```

### Windows Native
```ssh
Host levy
  HostName ssh.zazagaby.online
  User ai-dev
  IdentityFile "C:\Users\Me\.ssh\id_ed25519"
  ProxyCommand "C:\Windows\System32\cloudflared.exe" access ssh --hostname %h
```

---

## Security Architecture

**Dual-Layer Authentication:**
1. Cloudflare Zero Trust (Google SSO)
2. SSH Key (Ed25519)

**Public Endpoint:** ssh.zazagaby.online
**Authorized Users:** fazaasro@gmail.com, gabriela.servitya@gmail.com

---

## Next Steps

1. **Manual Action Required:**
   - Update `/etc/cloudflared/config.yml` (see SSH_CONFIG_UPDATE_NEEDED.md)
   - Restart cloudflared
   - Test SSH connection

2. **Client Setup:**
   - Install cloudflared on client
   - Configure `.ssh/config`
   - Install VS Code Remote - SSH extension

---

*Project Levy infrastructure prepared. Awaiting SSH rule deployment.*
