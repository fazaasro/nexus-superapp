# Google Calendar Integration Setup

**For:** Levy (Agent Faza)  
**Purpose:** Add Google Calendar + Gmail + Drive to OpenClaw  
**Method:** gog skill (Google OAuth CLI)

---

## Overview

The `gog` skill enables OpenClaw to:
- ✅ **Gmail** — Read, search, draft, send emails
- ✅ **Google Calendar** — Check schedule, find availability, create events
- ✅ **Google Drive** — Search files, read documents, organize folders
- ✅ **Google Docs/Sheets** — Query content, add rows, get summaries

---

## Setup Steps

### Step 1: Install gog Skill

```bash
# Option A: Via ClawHub (recommended)
clawdhub install gog

# Option B: Manual install
npm install -g gog
```

### Step 2: Create Google Cloud Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use existing)
3. **Enable APIs:**
   - Gmail API
   - Calendar API
   - Drive API
4. Create OAuth 2.0 credentials:
   - **Application type:** Desktop app
   - **Download JSON** (save as `credentials.json`)

### Step 3: Authenticate

```bash
gog auth
```

This opens your browser. Sign in, grant permissions, done!

### Step 4: Test

```bash
# Check emails
gog mail list

# Check calendar
gog calendar today

# Check this week
gog calendar week
```

---

## Calendar Commands (Once Set Up)

| Command | Purpose |
|---------|---------|
| `gog calendar today` | Show today's events |
| `gog calendar week` | Show this week's schedule |
| `gog calendar list` | List upcoming events |
| `gog calendar find "meeting"` | Search events |
| `gog calendar create` | Create new event |

---

## Examples

### What's My Schedule?
```
You: What's my week look like?
Me: [Uses gog calendar week]
    Here's your schedule for this week:
    - Mon Feb 10: Standup at 10am, Client call at 2pm
    - Tue Feb 11: Team standup at 9am
    - Wed Feb 12: No meetings
    - Thu Feb 13: Review with Sarah at 3pm
    - Fri Feb 14: Pre-reunion gathering (14:00-16:00)
```

### When Am I Free?
```
You: When am I free Thursday afternoon?
Me: [Uses gog calendar list]
    You're free Thursday afternoon:
    - Available: 1:00 PM - 5:00 PM
    - No conflicts found
```

### Add Event to Calendar
```
You: Add a team standup every Monday 9am
Me: [Uses gog calendar create]
    Event created:
    - Title: Team Standup
    - Start: Mondays at 9:00 AM
    - Recurring: Weekly
```

### Morning Briefing
```
You: Give me a rundown
Me:
    📅 Calendar:
      - 10am: Standup
      - 2pm: Client call
      - 4pm: 1:1 with Sarah

    📧 Email:
      - 8 unread, 2 flagged urgent

    ⚠️ Heads up:
      - Q4 report due Monday
```

---

## Adding IMT Alumni Events

Once gog is set up, I can add the IMT events for you:

### Event 1: Pre-Reunion Gathering
```bash
gog calendar create \
  --title "IMT Signum Pre-Reunion Gathering" \
  --start "2026-02-14T14:00:00" \
  --end "2026-02-14T16:00:00" \
  --location "Dreamcourt Grafika Sport Arena, Jl. Grafika No.58" \
  --description "Yuk kumpul dan mabar dulu sebelum acara Dies Natalis! 🤍"
```

### Event 2: Dies Natalis
```bash
gog calendar create \
  --title "Dies Natalis IMT 'Signum' ITB (10th Anniversary)" \
  --start "2026-02-21T15:00:00" \
  --end "2026-02-21T21:00:00" \
  --location "Gedung CRCS, ITB Kampus Ganesha" \
  --description "Gala Dinner + Campus Tour"
```

---

## Security & Privacy

- **OAuth Only** — Google's official OAuth 2.0, your password never exposed
- **Local Storage** — Tokens stored locally and encrypted
- **Granular Permissions** — Choose which services to enable
- **Revoke Anytime** — Remove access at [myaccount.google.com/permissions](https://myaccount.google.com/permissions)

---

## Troubleshooting

### "Access Denied" on OAuth
- Check that APIs are enabled in Google Cloud Console
- Verify OAuth app has correct scopes
- Run `gog auth --reset` to re-authenticate

### Calendar Events Missing
- Check calendar is set as primary
- Secondary calendars need explicit access
- Run `gog calendar list --all` to see all calendars

### Commands Not Working
- Verify gog is installed: `which gog`
- Check authentication: `gog auth status`
- Re-authenticate: `gog auth --reset`

---

## Related Integrations

| Integration | Status |
|-------------|--------|
| Gmail | ✅ Available (gog) |
| Google Calendar | ✅ Available (gog) |
| Google Drive | ✅ Available (gog) |
| Google Docs | ✅ Available (gog) |
| Google Sheets | ✅ Available (gog) |

---

*Setup guide created by Levy 🏗️*
*Reference: https://www.getopenclaw.ai/integrations/google-workspace*
