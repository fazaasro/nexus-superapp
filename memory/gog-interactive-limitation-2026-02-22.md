# gog CLI Interactive Limitation
**Date:** 2026-02-22 — 3:50 PM (Europe/Berlin)
**Agent:** Levy (Agent Faza)

---

## Problem

Cannot check emails or calendar via gog CLI in automated environment.

**Error Messages:**

**Email Check:**
```bash
gog mail list "is:unread"
# Error: missing --account (or set GOG_ACCOUNT, set default via `gog auth manage`, or store exactly one token)
```

**Calendar Check:**
```bash
gog calendar list "min_time=... max_time=..."
# Error: missing --account (or set GOG_ACCOUNT, set default via `gog auth manage`, or store exactly one token)
```

**Auth Status Check:**
```bash
gog auth list
# Error: read token for levynexus001@gmail.com: read token: no TTY available for keyring file backend password prompt; set GOG_KEYRING_PASSWORD
```

---

## Root Cause

**gog CLI requires interactive TTY for:**
- Keyring password prompts (stored tokens)
- Initial authentication flows

**OpenClaw exec limitation:**
- `exec` tool does not provide TTY (even with pty:true, the gog subprocess doesn't inherit it properly)
- Cannot enter passwords interactively
- Cannot access stored tokens in keyring

---

## Impact

**Cannot perform heartbeat tasks:**
- ✅ Memory maintenance - Can do (native tools)
- ✅ Health checks - Can do (docker commands)
- ❌ Email checking - Cannot do (gog needs TTY)
- ❌ Calendar checking - Cannot do (gog needs TTY)
- ❌ Weather - Could do via wttr.in if needed

---

## Workarounds

### Option 1: Use gog with Environment Variable
```bash
# Set password in environment (not secure)
export GOG_KEYRING_PASSWORD="your_password"
gog mail list "is:unread"
```

**Cons:** Not secure, password in environment

---

### Option 2: Configure gog for Non-Interactive Use
**Unknown if gog supports:**
- Config file with tokens
- Environment variable for token
- Different auth backend

**Need to research gog documentation.**

---

### Option 3: Alternative Tools
- **wttr.in** for weather (curl, no auth)
- **Web APIs** for calendar (if available)
- **Email notifications** via other means

---

## Status

| Heartbeat Task | Can I Do It? | Limitation |
|---------------|----------------|------------|
| Memory maintenance | ✅ Yes | None |
| Health checks | ✅ Yes | None |
| Email checking | ❌ No | gog needs TTY for keyring |
| Calendar checking | ❌ No | gog needs TTY for keyring |
| Weather | ✅ Yes | Use wttr.in (if needed) |

---

## Recommendation

**For heartbeat automation:**
1. Skip email/calendar checks (gog limitation)
2. Or set up gog with non-interactive auth (if possible)
3. Focus on memory maintenance + health checks

**For manual checks:**
- User can run gog commands directly in terminal (has TTY)
- Or I can guide user to check emails/calendar

---

*Limitation documented - gog requires interactive TTY*
