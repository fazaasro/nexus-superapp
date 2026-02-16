# Browser Integration Setup Guide

**For:** Levy (Agent Faza)  
**Purpose:** Enable OpenClaw Browser Control via Browser Relay

---

## 📋 Prerequisites

1. **Chrome or Edge browser** installed on your computer
2. **OpenClaw Browser Relay Extension** installed in Chrome
3. **OpenClaw Gateway** running and accessible

---

## 🚀 Setup Steps

### Step 1: Install Browser Relay Extension

1. Open Chrome/Edge on your computer
2. Go to Chrome Web Store
3. Search for: **OpenClaw Browser Relay**
4. Click "Add to Chrome"
5. Pin the extension to your toolbar (optional but recommended)

### Step 2: Connect Extension to Gateway

1. **On your computer**, navigate to:
   ```
   http://127.0.0.1:18789/
   ```
   OR via your public URL:
   ```
   https://agent.zazagaby.online/
   ```

2. Login with Google SSO (if using public URL)

3. Click the **OpenClaw Browser Relay** extension icon in your toolbar

4. The extension should show a badge (ON/OFF)

5. **Click the extension icon** to attach the current tab

6. You should see a confirmation message

### Step 3: Verify Connection

Run this command in OpenClaw to verify the browser is connected:

```bash
# I can run this:
browser action=start
```

If connected, I can see and interact with your browser tabs.

---

## 🔧 How It Works

### Two Modes

**1. openclaw Profile (Isolated)**
- Uses an isolated browser managed by OpenClaw
- Works without the extension
- Limited to certain websites

**2. chrome Profile (Your Browser)**
- Uses YOUR Chrome via Browser Relay extension
- Full control over your tabs
- Can access any site you're logged into

### Profile Selection

When I use browser control, I specify which profile:
```python
browser(
    action="start",
    profile="chrome"  # Use YOUR browser via Relay
)
# OR
browser(
    action="start",
    profile="openclaw"  # Use isolated browser
)
```

---

## 🎯 What I Can Do With Browser Control

### Actions
| Action | Description |
|--------|-------------|
| `snapshot` | Take a screenshot and analyze page |
| `navigate` | Go to a URL |
| `act` | Click, type, hover, etc. |
| `screenshot` | Save screenshot |
| `type` | Enter text in form fields |
| `click` | Click elements |
| `tabs` | List tabs |
| `focus` | Switch to tab |
| `close` | Close tab |

### Use Cases

1. **Web Testing** — Test your applications
2. **Data Extraction** — Scrape data from websites
3. **Form Filling** — Automate repetitive tasks
4. **Screenshot Capture** — Document pages
5. **Debugging** — Check how sites render
6. **Account Management** — Check status dashboards

---

## ⚠️ Security Considerations

### What I Can See
- The current tab you attach
- All elements on that page
- Text content
- Images

### What I Cannot See
- Other tabs (unless you switch to them)
- Passwords (they're masked)
- Private browsing mode tabs

### Best Practices

1. **Only attach when needed** — Don't keep tabs attached
2. **Check the badge** — Make sure extension is OFF when not in use
3. **Never share sensitive tabs** — Banking, personal accounts
4. **Review actions** — I'll tell you what I'm doing

---

## 🔄 Troubleshooting

### Issue: Extension Not Connecting

**Symptom:** Extension shows "OFF" or can't connect

**Solutions:**
1. Make sure OpenClaw Gateway is running
2. Check you're logged in to the Gateway UI
3. Try refreshing the page
4. Check browser console for errors (F12)

### Issue: Actions Not Working

**Symptom:** Browser tool commands fail

**Solutions:**
1. Make sure the tab is attached (badge says ON)
2. Refresh the page
3. Check the extension is enabled

### Issue: Gateway Not Accessible

**Symptom:** Can't reach `http://127.0.0.1:18789/`

**Solutions:**
1. Check if Gateway is running:
   ```bash
   ps aux | grep openclaw-gateway
   ```
2. If not running, restart it
3. Check if port 18789 is available

---

## 📝 Example Workflow

```bash
# 1. You open a tab and attach the extension

# 2. I take a snapshot to see the page
browser action=snapshot

# 3. I analyze and tell you what I see
"I see a dashboard with 3 charts..."

# 4. I click a button
browser action=act request='{"kind":"click","ref":"some-button"}'

# 5. I take another snapshot to confirm
browser action=snapshot
```

---

## 🔗 Quick Links

- **Gateway UI:** http://127.0.0.1:18789/ (local) or https://agent.zazagaby.online/ (public)
- **Chrome Web Store:** Search "OpenClaw Browser Relay"
- **OpenClaw Docs:** https://docs.openclaw.ai

---

## ✅ Checklist

- [ ] Install OpenClaw Browser Relay extension
- [ ] Gateway is running (accessible at http://127.0.0.1:18789/)
- [ ] Extension badge shows ON when tab is attached
- [ ] Can take snapshot from OpenClaw
- [ ] Can navigate to URLs
- [ ] Can click/type on pages

---

## 🆚 Brave Search vs Browser Control

| Feature | Brave Search | Browser Control |
|---------|---------------|-----------------|
| Search | ✅ Web search | ❌ No |
| Scrape | ✅ Extract content | ✅ Full page access |
| Interactive | ❌ Read-only | ✅ Click, type, scroll |
| Auth | ❌ No | ✅ Can use your logins |
| Screenshots | ❌ No | ✅ Yes |

**Best:** Use both together — Brave for search, Browser for interaction.

---

*Setup guide created by Levy 🏗️*
