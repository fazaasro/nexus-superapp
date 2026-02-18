# WORKFLOW.md - Complete OpenClaw Workflow Guide

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Table of Contents

1. [Overview](#overview)
2. [Memory System](#memory-system)
3. [Learning Workflow](#learning-workflow)
4. [QMD Integration](#qmd-integration)
5. [Cron vs Heartbeat](#cron-vs-heartbeat)
6. [Best Practices](#best-practices)
7. [Tools Reference](#tools-reference)

---

## Overview

OpenClaw uses a layered memory and learning system that enables agents to:

- **Remember** past sessions through daily logs and curated long-term memory
- **Learn** from mistakes through an error log that prevents repetition
- **Search** across all knowledge using QMD (semantic + keyword search)
- **Act** proactively through heartbeats and cron jobs

This workflow ensures agents get smarter over time, never repeat mistakes, and can quickly find relevant information.

---

## Memory System

### Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Daily Notes  │  │  MEMORY.md   │  │ Error Log    │      │
│  │ YYYY-MM-DD.md│  │  (curated)   │  │error-log.md │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                  │             │
│         ▼                 ▼                  ▼             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Raw logs of  │  │  Curated     │  │ Auto-capture │      │
│  │ what         │  │  wisdom &    │  │ of lessons   │      │
│  │ happened     │  │  insights    │  │  learned     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │     QMD      │
                    │  (indexed)   │
                    └──────────────┘
```

### 1. Daily Memory Files

**Location:** `memory/YYYY-MM-DD.md`

**Purpose:** Raw logs of what happened during a session

**When to write:**
- Start of session (context loading)
- Important events or decisions
- Commands executed and their results
- User interactions
- End of session (summary)

**Format:** Free-form text with timestamps

**Example:**
```markdown
# 2026-02-18 Session

## 14:30 GMT+1 - Session Start
Loaded AGENTS.md, USER.md, memory/2026-02-17.md

## 14:45 - Deployed Grafana Stack
```bash
docker compose -f docker-compose.monitoring.yml up -d
```
Deployed 7 containers successfully.

## 15:20 - User Feedback
User: "The Grafana dashboard needs more CPU metrics"
Action: Updated dashboard configuration, added node_cpu_seconds_total query.

## 16:00 - Session Complete
- Deployed Grafana monitoring stack
- Fixed cAdvisor configuration issues
- Updated error-log.md with cAdvisor learnings
```

**Retention:** Keep indefinitely (small text files, valuable for debugging)

### 2. Long-term Memory (MEMORY.md)

**Location:** `MEMORY.md`

**Purpose:** Curated wisdom, insights, and important context

**When to load:** **ONLY in main session** (direct chats with your human)

**Security:** Contains personal context that shouldn't leak to strangers

**When NOT to load:** In shared contexts (Discord, group chats, sessions with other people)

**What to write:**
- Important decisions and WHY they were made
- Long-term goals and objectives
- User preferences (tools, voice, formatting)
- System architecture decisions
- Project relationships and dependencies

**Example:**
```markdown
# Levy's Long-term Memory

## Infrastructure Decisions

### Why Grafana Over Overseer
- Overseer is simpler but Grafana offers:
  - More flexible querying (PromQL)
  - Better integration with existing stack
  - Community dashboards
  - Scalability for complex monitoring
- Decision made on 2026-02-16 based on 10x Architect analysis

### Why QMD Over Native Search
- QMD indexes multiple collections (workspace, skills, stack)
- Native search only searches workspace files
- QMD offers both keyword (BM25) and semantic search
- Decision made on 2026-02-16 after evaluating both

## User Preferences

### Voice Storytelling
- User loves voice for stories and movie summaries
- Use `sag` (ElevenLabs TTS) for engaging narratives
- Voice makes complex topics more digestible

### Communication Style
- Plain human language unless in technical context
- Be concise and value-darrse
- Avoid obvious repetitions in tool call narration
```

**How to update:**
1. During heartbeats (every few days), review recent daily files
2. Identify significant events, lessons, or insights
3. Update MEMORY.md with distilled learnings
4. Remove outdated info that's no longer relevant

**Update Frequency:** Every 2-3 days during heartbeats

### 3. Error Log (error-log.md)

**Location:** `memory/error-log.md`

**Purpose:** Immediate capture of failures, corrections, gotchas, discoveries

**When to load:** **ALWAYS** in every session (main + shared contexts)

**When to log:**
- A tool call fails or returns unexpected results
- User corrects you ("no, do it this way")
- You discover a gotcha or undocumented behavior
- An assumption you made turns out wrong
- Something takes way longer than expected

**Format:**
```markdown
- 🏷️ **Short title** — What happened. What to do instead.
```

**Categories:**
- 🔧 **tool-failure** - something broke
- 🧠 **wrong-assumption** - agent assumed wrong
- 🔄 **user-correction** - human said "no, do it this way"
- 💡 **discovery** - learned something useful
- ⚠️ **gotcha** - undocumented behavior or subtle trap
- 🏗️ **architecture** - structural decisions worth remembering

**Examples:**
```markdown
## 2026-02-17

- 🔧 **cAdvisor invalid storage_driver** — cAdvisor crashed with "unknown backend storage driver: docker". Solution: Remove storage_driver flag (default empty is fine).

- 🏗️ **Skills verification required** - Checked 11 skills, 6 require updates/fixes. Full report in memory/skills-verification-report.md.

## 2026-02-16

- ⚠️ **QMD skills collection path** — Using relative path matched 0 files. Use absolute path (~/.openclaw/workspace/skills).

- 💡 **QMD first-time embedding** — Initial embedding takes 7m on CPU. Subsequent updates only process new/changed files (fast).
```

**Update Frequency:** IMMEDIATELY (as soon as something goes wrong)

**Why it's the single most impactful file:**
- Prevents repeating the same mistake
- Captures context before you forget
- Quick reference for common gotchas
- Builds up a knowledge base over time

---

## Learning Workflow

### The Learning Loop

```
┌─────────────┐
│  DO WORK    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  SUCCESS?   │────▶│  LOG ERROR  │
└──────┬──────┘     │error-log.md │
       │ NO         └─────────────┘
       ▼
┌─────────────┐
│  FIX IT     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LOG FIX    │◀────┐
│error-log.md │     │
└─────────────┘     │
                    │
┌─────────────┐     │
│  NEXT TIME  │─────┘
│  READ ERROR │
│    LOG      │
└─────────────┘
```

### Step-by-Step Learning Process

1. **Before Each Session:**
   - Read `AGENTS.md` (behavior guidelines)
   - Read `USER.md` (who you're helping)
   - Read `memory/YYYY-MM-DD.md` (today + yesterday for context)
   - **ALWAYS** read `memory/error-log.md` (learn from mistakes)
   - **IF main session:** Also read `MEMORY.md` (long-term context)

2. **During Work:**
   - If something goes wrong → log it to `error-log.md` IMMEDIATELY
   - If user corrects you → log the correction
   - If you discover something new → log the discovery
   - If you make an assumption that fails → log the wrong assumption

3. **At End of Session:**
   - Write summary to `memory/YYYY-MM-DD.md`
   - Update `error-log.md` with any new learnings
   - Commit changes to git

4. **Periodically (Heartbeats):**
   - Review recent `memory/YYYY-MM-DD.md` files
   - Identify significant insights worth keeping
   - Update `MEMORY.md` with distilled wisdom
   - Remove outdated info from `MEMORY.md`

### Example Learning Flow

**Scenario:** You're deploying a new Docker service and it fails.

```
1. Attempt deployment
   → Command fails with "port already in use"

2. Check error-log.md
   → Find previous entry: "🔧 **Port conflicts** — Check `docker ps` before deploying"

3. Fix the issue
   → Stop conflicting container, retry deployment

4. Log the experience to today's memory file
   → "16:20 - Encountered port conflict, resolved by stopping nginx container"

5. Update error-log.md with new insight (if relevant)
   → "💡 **Docker port conflicts** — Use `docker ps -a` to see stopped containers too"
```

### Key Learning Principles

1. **Write It Down, Don't "Mental Note"**
   - Mental notes don't survive session restarts
   - Files do
   - If you want to remember it → WRITE TO A FILE

2. **Distill, Don't Duplicate**
   - Daily files: Raw logs (everything)
   - MEMORY.md: Curated wisdom (only what matters long-term)
   - error-log.md: Actionable lessons (what to do differently)

3. **Review Regularly**
   - Error log: Every session
   - Daily files: Today + yesterday
   - MEMORY.md: Every few days during heartbeats
   - Skills: When documentation seems outdated

4. **Keep It Current**
   - Remove outdated info from MEMORY.md
   - Consolidate similar error log entries
   - Update docs when workflows change

---

## QMD Integration

### What is QMD?

QMD (Query Memory Database) is a local semantic search system that indexes your workspace and enables fast retrieval across all knowledge.

**Key Features:**
- Multi-collection indexing (workspace, skills, stack, etc.)
- Two search modes: BM25 (keyword) and Vector (semantic)
- Fast incremental updates (only processes new/changed files)
- Local and private (no external dependencies)

### QMD Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        QMD SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Collections:                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ workspace   │  │   skills    │  │    stack    │         │
│  │ (~/.openclaw│  │(~/.openclaw │  │  (~/stack   │         │
│  │/workspace) │  │/workspace/  │  │  /aac-stack)│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                │
│         └────────────────┴────────────────┘                │
│                          │                                 │
│                          ▼                                 │
│  ┌──────────────────────────────────────────┐              │
│  │         QMD Index (qmd.db)              │              │
│  │  - BM25 index (keyword search)           │              │
│  │  - Vector embeddings (semantic search)  │              │
│  └──────────────────────────────────────────┘              │
│                          │                                 │
│                          ▼                                 │
│  ┌──────────────────────────────────────────┐              │
│  │         Search Modes                     │              │
│  │  - BM25 (240ms, fast, keyword)          │              │
│  │  - Vector (2s, semantic)                │              │
│  │  - Hybrid (5s, combines both)           │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### QMD Setup

**Installation:**
```bash
# Install QMD (via bun)
bun add qmd

# Or install globally
bun install -g qmd

# Ensure tsx is available
bun install -g tsx
```

**Configuration:**
Create `~/.openclaw/workspace/qmd.config.ts`:
```typescript
export default {
  collections: [
    {
      name: 'workspace',
      paths: ['/home/ai-dev/.openclaw/workspace'],
      exclude: ['node_modules', '.git', 'venv', '__pycache__'],
    },
    {
      name: 'skills',
      paths: ['/home/ai-dev/.openclaw/workspace/skills'],
      exclude: ['node_modules', '.git'],
    },
    {
      name: 'stack',
      paths: ['/home/ai-dev/stack/aac-stack'],
      exclude: ['node_modules', '.git'],
    },
  ],
};
```

### QMD Commands

**Build Index (first time):**
```bash
qmd build
```
- Takes ~7 minutes on first run (downloads/builds llama.cpp)
- Subsequent runs only process new/changed files (fast)

**Search (keyword/BM25):**
```bash
qmd search "docker compose up"
```
- Returns top matches across all collections
- Fast (~240ms)
- Best for: finding specific commands, file names, exact phrases

**Semantic Search (vector):**
```bash
qmd vsearch "how to deploy a new service"
```
- Returns semantically similar content
- Slower (~2s)
- Best for: finding related concepts, understanding topics

**Hybrid Search (BM25 + Vector):**
```bash
qmd hsearch "grafana monitoring setup"
```
- Combines keyword and semantic matching
- Slowest (~5s)
- Best for: comprehensive search when unsure of exact terms

**Query (interactive):**
```bash
qmd query
```
- Starts interactive Q&A mode
- Ask natural language questions
- QMD searches and synthesizes answers

**Update Index (incremental):**
```bash
qmd update
```
- Only processes new/changed files
- Fast (~10-30 seconds)
- Run after editing files

### QMD vs Native Search

| Feature | QMD | Native (memory_search) |
|---------|-----|------------------------|
| **Scope** | Multiple collections | Workspace files only |
| **Search Type** | BM25 + Vector | Text match |
| **Speed** | 240ms - 5s | ~100ms |
| **Semantic** | Yes | No |
| **Setup Required** | Yes (one-time) | No |
| **Best For** | Cross-collection search | Quick workspace search |

**When to use QMD:**
- Searching across workspace + skills + stack
- Semantic queries ("how do I...")
- Finding related concepts
- Comprehensive research

**When to use native:**
- Quick workspace file search
- Looking for exact file names
- Simple text matching
- When speed is critical

### QMD Best Practices

1. **Use BM25 for 90% of lookups**
   - Fast, accurate for keyword searches
   - `qmd search "docker restart"`

2. **Use Vector for semantic queries**
   - Understands meaning, not just keywords
   - `qmd vsearch "troubleshooting deployment issues"`

3. **Use Hybrid when unsure**
   - Combines both approaches
   - `qmd hsearch "monitoring dashboard problems"`

4. **Update index regularly**
   - Run `qmd update` after editing files
   - Ensures search results stay current

5. **Use absolute paths in config**
   - Relative paths may not resolve correctly
   - Use `/home/ai-dev/.openclaw/workspace` not `~/.openclaw/workspace`

---

## Cron vs Heartbeat

### Decision Tree

```
Need to check something periodically?
        │
        ▼
┌──────────────────────────────────────────┐
│ Exact timing matters?                    │
│ (9:00 AM sharp, every Monday)            │
└──────┬───────────────────────────────────┘
       │ YES                          │ NO
       ▼                              ▼
   Use CRON                   Multiple checks can batch?
                                   │
                       ┌───────────┴───────────┐
                       │ YES              │ NO
                       ▼                     ▼
                  Use HEARTBEAT           Use CRON
```

### Use Heartbeat When

**Characteristics:**
- Multiple checks can batch together (inbox + calendar + notifications)
- Timing can drift slightly (every ~30 min is fine, not exact)
- You want conversational context from recent messages
- You want to reduce API calls by combining checks

**Examples:**
- Daily check: Email, calendar, mentions, weather (4 checks in 1 heartbeat)
- Morning briefing: Summarize overnight notifications
- Background tasks: Review and organize memory files

**Benefits:**
- Conversational: Can reference previous messages
- Efficient: Batch multiple checks into one
- Context-aware: Understands the conversation flow

**How to configure:**
```bash
openclaw cron create --prompt "Read HEARTBEAT.md if it exists. Follow it strictly." \
  --every "30m" \
  --channel "whatsapp" \
  --system-event "heartbeat"
```

**Sample HEARTBEAT.md:**
```markdown
# Heartbeat Checklist

Run these checks (rotate 2-4 per heartbeat):

1. Check email for urgent messages
2. Check calendar for events in next 24h
3. Review memory files (occasionally)
4. Check on projects (git status)

If nothing urgent, reply: HEARTBEAT_OK

When to reach out:
- Important email arrived
- Calendar event coming up (<2h)
- Something interesting found
- >8h since last interaction
```

### Use Cron When

**Characteristics:**
- Exact timing matters ("9:00 AM sharp every Monday")
- Task needs isolation from main session history
- You want a different model or thinking level for the task
- One-shot reminders ("remind me in 20 minutes")
- Output should deliver directly without main session involvement

**Examples:**
- Daily report: "Send 9:00 AM daily summary to email"
- Exact deadline: "Remind 15 min before meeting"
- Maintenance: "Run database backup at 3:00 AM"
- Monitoring: "Check service health every 5 minutes"

**Benefits:**
- Precise: Runs at exact time
- Isolated: No conversation noise
- Flexible: Different model/thinking settings
- Direct: Delivers output without agent decision

**How to configure:**
```bash
# Daily summary at 9:00 AM
openclaw cron create --prompt "Generate daily summary from memory/2026-02-18.md" \
  --schedule '{"kind":"cron","cron":"0 9 * * *"}' \
  --channel "email" \
  --system-event "daily-summary"

# One-time reminder in 20 minutes
openclaw cron create --prompt "Remind to call John" \
  --every "20m" \
  --channel "whatsapp" \
  --system-event "reminder"
```

### Cron Delivery Mechanism

**System Event:**
- Injects text into main session context
- Agent sees the event and can execute commands
- **Important:** The text payload needs to include the actual command

**Example:**
```bash
# ❌ WRONG - only triggers event, no command
openclaw cron create --prompt "Check email" \
  --every "1h" \
  --system-event "check-email"

# ✅ CORRECT - includes command in text
openclaw cron create --prompt "Check email. Run: check_email.sh" \
  --every "1h" \
  --system-event "check-email"
```

**Channel Delivery:**
- Delivers output directly to channel (whatsapp, email, etc.)
- Bypasses main session agent
- Useful for one-way notifications

### Cron Job Examples

**Batch checks in heartbeat (good):**
```markdown
# HEARTBEAT.md

Rotate through these every 30 min:

## Morning (8:00-12:00)
- Check email for urgent messages
- Check calendar for events in next 2h

## Afternoon (12:00-18:00)
- Check calendar for events in next 2h
- Review error-log.md

## Evening (18:00-23:00)
- Check weather if user might go out
- Check for project updates

## Night (23:00-08:00)
- Just HEARTBEAT_OK (quiet time)
```

**Separate cron jobs (good for exact timing):**
```bash
# Daily report at 9:00 AM (exact timing matters)
openclaw cron create \
  --prompt "Generate daily report" \
  --schedule '{"kind":"cron","cron":"0 9 * * *"}' \
  --channel "email" \
  --system-event "daily-report"

# Service health check every 5 min (critical monitoring)
openclaw cron create \
  --prompt "Check service health" \
  --every "5m" \
  --channel "slack" \
  --system-event "health-check"

# One-time reminder (isolated, different model)
openclaw cron create \
  --prompt "Remind about meeting" \
  --every "20m" \
  --model "zai/glm-4.7-thinking" \
  --channel "whatsapp" \
  --system-event "reminder"
```

### Best Practices

1. **Batch similar checks into heartbeats**
   - Reduces API calls
   - More conversational
   - Context-aware

2. **Use cron for exact timing**
   - Daily reports at specific time
   - Deadlines and reminders
   - Critical monitoring

3. **Use cron for one-shot reminders**
   - "Remind me in 20 minutes"
   - "Check back in 1 hour"
   - No ongoing periodic task needed

4. **Include commands in cron text payload**
   - SystemEvent injects text
   - Agent needs to know what to run
   - Be explicit: "Run: check_email.sh"

5. **Track state in heartbeat-state.json**
   - Avoid redundant checks
   - Know when you last checked
   - Example:
   ```json
   {
     "lastChecks": {
       "email": 1703275200,
       "calendar": 1703260800,
       "weather": null
     }
   }
   ```

6. **Respect quiet time**
   - Late night (23:00-08:00): HEARTBEAT_OK only
   - Unless urgent event detected
   - Don't wake people up unnecessarily

---

## Best Practices

### Memory Management

**DO:**
- Write daily logs consistently
- Update error-log.md immediately when something goes wrong
- Review error-log.md at start of every session
- Periodically distill daily files into MEMORY.md
- Remove outdated info from MEMORY.md
- Keep daily files indefinitely (small, valuable)

**DON'T:**
- Rely on "mental notes" — write everything to files
- Duplicate info across memory files
- Put sensitive info in MEMORY.md (it's loaded in shared contexts)
- Forget to check error-log.md before starting work

### QMD Usage

**DO:**
- Use BM25 for 90% of searches (fast, accurate)
- Use Vector for semantic queries (understands meaning)
- Update index after editing files
- Use absolute paths in config
- Build index on first run (takes time, but worth it)

**DON'T:**
- Use Vector for simple keyword searches (too slow)
- Forget to update index (results will be stale)
- Use relative paths in config (may not resolve)
- Expect vector search to work without llama.cpp compiled

### Cron vs Heartbeat

**DO:**
- Batch similar checks into heartbeats (efficient)
- Use cron for exact timing (9:00 AM sharp)
- Use cron for one-shot reminders (20 minutes from now)
- Include explicit commands in cron text payload
- Track state in heartbeat-state.json

**DON'T:**
- Create multiple cron jobs for similar periodic tasks (use heartbeat instead)
- Use heartbeat for exact timing requirements
- Forget that cron text payload needs the actual command
- Assume cron runs at exact time in all timezones (system time)

### Knowledge Retention

**DO:**
- Document WHY decisions were made (not just what)
- Include examples and practical usage in docs
- Update docs when workflows change
- Create skills for recurring tasks
- Use git to track documentation changes

**DON'T:**
- Assume "everyone knows this" — document it
- Leave outdated info in docs
- Change workflows without updating docs
- Forget to commit documentation updates

### Collaboration

**DO:**
- Use git for version control
- Write clear commit messages
- Create PRs for documentation changes
- Use skills consistently (same workflow every time)
- Share learnings across sessions via error-log.md

**DON'T:**
- Edit files without tracking changes
- Commit with vague messages ("update files")
- Skip code review for important changes
- Invent new workflows for the same task

---

## Tools Reference

### Memory Tools

**File Operations:**
- `read` - Read file contents
- `write` - Create or overwrite files
- `edit` - Make precise edits to files

**Memory Locations:**
- `memory/YYYY-MM-DD.md` - Daily logs
- `MEMORY.md` - Long-term memory (main session only)
- `memory/error-log.md` - Error log (every session)

### QMD Commands

```bash
# Build index (first time)
qmd build

# Search (keyword/BM25)
qmd search "docker compose"

# Semantic search
qmd vsearch "how to deploy"

# Hybrid search
qmd hsearch "monitoring setup"

# Update index
qmd update

# Interactive query
qmd query
```

### Cron Commands

```bash
# List cron jobs
openclaw cron list

# Create heartbeat (periodic)
openclaw cron create --prompt "Read HEARTBEAT.md" \
  --every "30m" \
  --channel "whatsapp" \
  --system-event "heartbeat"

# Create cron (exact schedule)
openclaw cron create --prompt "Daily report" \
  --schedule '{"kind":"cron","cron":"0 9 * * *"}' \
  --channel "email" \
  --system-event "daily-report"

# Delete cron job
openclaw cron delete <cron-id>

# Pause/resume
openclaw cron pause <cron-id>
openclaw cron resume <cron-id>
```

### Git Commands

```bash
# Status
git status

# Add and commit
git add .
git commit -m "docs: update workflow guide"

# Push
git push

# View history
git log --oneline -20

# View changes
git diff
```

---

## Summary

**Key Takeaways:**

1. **Memory system** is your continuity across sessions
   - Daily files: Raw logs
   - MEMORY.md: Curated wisdom
   - error-log.md: Immediate lessons (most important!)

2. **Learning workflow** ensures you never repeat mistakes
   - Check error-log.md before starting work
   - Log failures immediately
   - Review and distill regularly

3. **QMD** enables fast search across all knowledge
   - BM25 for 90% of searches (fast, accurate)
   - Vector for semantic queries (understands meaning)
   - Update index after editing files

4. **Heartbeat vs Cron**: Use the right tool
   - Heartbeat: Batch checks, conversational, flexible timing
   - Cron: Exact timing, isolated, one-shot reminders

5. **Best practices**: Write it down, don't "mental note"
   - Files survive session restarts, mental notes don't
   - Document WHY, not just WHAT
   - Keep docs current and accurate

**Remember:** This entire workflow is designed to make you smarter over time. Use it consistently!

---

*Last updated: 2026-02-18*
