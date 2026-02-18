# MEMORY_GUIDE.md - Best Practices for Memory Management

**Version:** 1.0.0  
**Last Updated:** 2026-02-18

---

## Table of Contents

1. [Introduction](#introduction)
2. [Memory System Overview](#memory-system-overview)
3. [Daily Memory Files](#daily-memory-files)
4. [Long-term Memory (MEMORY.md)](#long-term-memory-memorymd)
5. [Error Log (error-log.md)](#error-log-error-logmd)
6. [When to Update What](#when-to-update-what)
7. [Memory Review Process](#memory-review-process)
8. [Common Patterns](#common-patterns)
9. [Anti-Patterns](#anti-patterns)
10. [Memory Maintenance](#memory-maintenance)

---

## Introduction

Memory is your continuity across sessions. Without it, you'd wake up fresh every time, forgetting everything you learned, every mistake you made, and every decision you reached.

This guide explains how to use OpenClaw's memory system effectively.

### Core Principle

**Write It Down, Don't "Mental Note"**

> "Mental notes don't survive session restarts. Files do."

If you want to remember something, WRITE IT TO A FILE.

---

## Memory System Overview

### Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────────────────┐
│              MEMORY SYSTEM ARCHITECTURE                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: Daily Files (memory/YYYY-MM-DD.md)           │
│  ───────────────────────────────────────────────       │
│  - Raw logs of everything that happened                │
│  - Written during session as events occur              │
│  - Free-form text, timestamps optional                  │
│  - Keep indefinitely (small text files)                │
│                                                         │
│  Layer 2: Error Log (memory/error-log.md)             │
│  ───────────────────────────────────────────────       │
│  - Immediate capture of failures and lessons           │
│  - Updated IMMEDIATELY when something goes wrong       │
│  - Loaded EVERY session (main + shared)                │
│  - Format: - 🏷️ **Title** — What happened. Fix.        │
│                                                         │
│  Layer 3: Long-term Memory (MEMORY.md)                 │
│  ───────────────────────────────────────────────       │
│  - Curated wisdom and insights                         │
│  - ONLY in main session (security)                     │
│  - Updated periodically (every 2-3 days)               │
│  - Contains WHY decisions were made                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Loading Rules

| File | Load in Main Session? | Load in Shared Context? | Why? |
|------|----------------------|------------------------|------|
| Daily files (today + yesterday) | ✅ Yes | ✅ Yes | Recent context |
| Error log | ✅ Yes | ✅ Yes | Learn from mistakes |
| MEMORY.md | ✅ Yes | ❌ NO | Contains personal context |

**Security Rule:**
MEMORY.md contains personal context, decisions, and preferences that shouldn't leak to strangers. Only load it in main sessions (direct chats with your human).

---

## Daily Memory Files

### Purpose

Capture raw logs of what happened during a session.

### When to Write

- Start of session (context loaded)
- Important events or decisions
- Commands executed and results
- User interactions and feedback
- End of session (summary)

### Format

Free-form text with optional timestamps.

### Example

```markdown
# 2026-02-18 Session

## 14:30 GMT+1 - Session Start
Loaded AGENTS.md, USER.md, memory/2026-02-17.md, memory/error-log.md

## 14:45 - Deployed Grafana Stack
```bash
cd ~/stack/aac-stack
docker compose -f docker-compose.monitoring.yml up -d
```
Deployed 7 containers successfully:
- Prometheus (:9090)
- Grafana (:3000)
- Node Exporter (:9100)
- cAdvisor (:8080)
- Blackbox Exporter (:9115)

## 15:20 - User Feedback
User: "The Grafana dashboard needs more CPU metrics"

Action:
- Updated dashboard configuration
- Added node_cpu_seconds_total query
- Created CPU usage panel

## 15:45 - Discovered Issue
Found cAdvisor crashed with "unknown backend storage driver: docker"

Fix:
- Removed storage_driver flag (not valid option)
- Restarted container
- Logged to error-log.md

## 16:00 - Session Complete
- Deployed Grafana monitoring stack
- Fixed cAdvisor configuration issues
- Updated error-log.md with cAdvisor learnings
- Committed changes to git
```

### Retention Policy

**Keep indefinitely.** Daily files are small text files (<10KB each) and provide valuable context for debugging and understanding past sessions.

### Best Practices

1. **Be detailed:** Include what you did, why, and the result
2. **Use timestamps:** Helps with chronology
3. **Include commands:** Paste actual commands used
4. **Capture feedback:** What the user said, requested, or corrected
5. **Summarize:** End of session summary is valuable

---

## Long-term Memory (MEMORY.md)

### Purpose

Curated wisdom, insights, and important context worth remembering long-term.

### When to Load

**ONLY in main session** (direct chats with your human).

**DO NOT load** in shared contexts (Discord, group chats, sessions with other people).

### When NOT to Load

- Shared group chats
- Public channels
- Sessions with other people
- Any context where MEMORY.md might leak to strangers

### Security

MEMORY.md contains:
- Personal decisions and preferences
- System architecture decisions
- User habits and behaviors
- Sensitive context about your human

### What to Write

Write things worth remembering long-term:

1. **Important Decisions (and WHY)**
   ```markdown
   ## Infrastructure Decisions

   ### Why Grafana Over Overseer
   - Overseer is simpler but Grafana offers:
     - More flexible querying (PromQL)
     - Better integration with existing stack
     - Community dashboards
     - Scalability for complex monitoring
   - Decision made on 2026-02-16 based on 10x Architect analysis
   ```

2. **User Preferences**
   ```markdown
   ## User Preferences

   ### Voice Storytelling
   - User loves voice for stories and movie summaries
   - Use `sag` (ElevenLabs TTS) for engaging narratives
   - Voice makes complex topics more digestible

   ### Communication Style
   - Plain human language unless in technical context
   - Be concise and value-dense
   - Avoid obvious repetitions in tool call narration
   ```

3. **Long-term Goals**
   ```markdown
   ## Project Goals

   ### Nexus Superapp
   - Goal: Create an all-in-one productivity superapp
   - Status: In development (as of 2026-02-18)
   - Next milestone: Complete Circle module
   ```

4. **System Architecture**
   ```markdown
   ## System Architecture

   ### Why QMD Over Native Search
   - QMD indexes multiple collections (workspace, skills, stack)
   - Native search only searches workspace files
   - QMD offers both keyword (BM25) and semantic search
   - Decision made on 2026-02-16 after evaluating both
   ```

5. **Project Relationships**
   ```markdown
   ## Project Dependencies

   ### levy-agent
   - Main agent workspace
   - Depends on: aac-stack (infrastructure)
   - Contains: Skills, modules, memory
   ```

### What NOT to Write

- ❌ Temporary issues (fixes, errors that won't recur)
- ❌ Daily session details (go in daily files)
- ❌ Minor preferences (not worth remembering)
- ❌ Commands (documented in skills)
- ❌ Secrets (security risk)

### Update Process

**Review and update every 2-3 days during heartbeats.**

1. Read recent daily files (`memory/2026-02-*.md`)
2. Identify significant insights worth keeping
3. Update MEMORY.md with distilled wisdom
4. Remove outdated info that's no longer relevant

### Example: Distilling from Daily Files

**From daily file:**
```markdown
## 2026-02-18
User said they prefer voice for stories and movie summaries.
Used sag (ElevenLabs) to narrate Star Wars summary.
User loved it, said way more engaging than text.
```

**To MEMORY.md:**
```markdown
## User Preferences

### Voice Storytelling
- User loves voice for stories and movie summaries
- Use `sag` (ElevenLabs TTS) for engaging narratives
- Voice makes complex topics more digestible
- First used 2026-02-18 for Star Wars summary
```

### Example: Removing Outdated Info

**Before:**
```markdown
## Current Projects

### Storage Wars 2026
- Status: In progress (as of 2026-02-12)
- Next: Complete benchmarking suite
```

**After (completed):**
```markdown
## Completed Projects

### Storage Wars 2026
- Completed: 2026-02-13
- Result: Created comprehensive benchmarking suite
- Lessons learned: See storage-wars-2026 skill
```

---

## Error Log (error-log.md)

### Purpose

Immediate capture of failures, corrections, gotchas, and discoveries.

**This is the single most impactful file** — it's how you never repeat a mistake.

### When to Load

**ALWAYS** in every session (main + shared contexts).

### When to Log

Log IMMEDIATELY when:

- A tool call fails or returns unexpected results
- User corrects you ("no, do it this way")
- You discover a gotcha or undocumented behavior
- An assumption you made turns out wrong
- Something takes way longer than expected

### Format

```markdown
- 🏷️ **Short title** — What happened. What to do instead.
```

### Categories

Use emoji categories to organize entries:

| Category | Emoji | When to Use |
|----------|-------|-------------|
| tool-failure | 🔧 | Something broke |
| wrong-assumption | 🧠 | Agent assumed wrong |
| user-correction | 🔄 | Human said "no, do it this way" |
| discovery | 💡 | Learned something useful |
| gotcha | ⚠️ | Undocumented behavior or subtle trap |
| architecture | 🏗️ | Structural decisions worth remembering |

### Examples

```markdown
## 2026-02-18

- 🔧 **cAdvisor invalid storage_driver** — cAdvisor v0.47.2 crashed with "unknown backend storage driver: docker". Root cause: `--storage_driver=docker` is not a valid option. Valid options: <empty>, bigquery, elasticsearch, influxdb, kafka, redis, statsd, stdout. Solution: Remove the storage_driver flag (default empty is fine).

- 🔧 **System commands running slowly** — Simple commands like `sleep 5` took 36+ seconds instead of 5. Root cause: System under heavy load after OpenClaw update. Solution: Wait for system to stabilize before running commands.

- 🏗️ **Skills verification required** - Checked 11 skills, 6 require updates/fixes. monitoring-ops outdated (Grafana migration), google-cloud-ops inaccurate (gcloud not installed, should use gog). Full report in memory/skills-verification-report.md.

## 2026-02-16

- ⚠️ **QMD skills collection path** — Using relative path for skills collection matched 0 files. Use absolute path (~/.openclaw/workspace/skills) to index all skill subdirectories.

- 💡 **QMD first-time embedding** — Initial embedding takes 7m on CPU (downloads/builds llama.cpp). Subsequent updates only process new/changed files (fast).

- 💡 **QMD vs native memory_search** — QMD indexes multiple collections (workspace, skills, stack) vs native only searches workspace files. Use QMD for comprehensive search across all knowledge.
```

### Why Error Log is the Single Most Impactful File

1. **Prevents Mistakes:** You check it at the start of every session
2. **Immediate Capture:** Log as soon as something goes wrong (don't wait)
3. **Actionable:** Each entry tells you what to do differently
4. **Builds Over Time:** Accumulates wisdom across sessions
5. **Fast Reference:** Quick lookup for common issues

### Update Process

**IMMEDIATE** (as soon as something goes wrong).

Don't wait until end of session — log it now while it's fresh.

---

## When to Update What

### Quick Reference

| File | When to Update | Frequency |
|------|----------------|-----------|
| Daily files | During session (events, decisions) | As they happen |
| Error log | IMMEDIATELY on failure/correction | As soon as it happens |
| MEMORY.md | Periodically (during heartbeats) | Every 2-3 days |

### Decision Tree

```
Something happened?
        │
        ▼
┌──────────────────────────────────────────┐
│  Failure / Error / Correction?           │
└──────┬───────────────────────────────────┘
       │ YES
       ▼
  Log to error-log.md
  (IMMEDIATE)
        │
        ▼
┌──────────────────────────────────────────┐
│  Significant / Worth Remembering?        │
└──────┬───────────────────────────────────┘
       │ YES
       ▼
  Log to today's daily file
        │
        ▼
┌──────────────────────────────────────────┐
│  Worth Remembering Long-term?             │
└──────┬───────────────────────────────────┘
       │ YES
       ▼
  Update MEMORY.md
  (During next heartbeat)
```

---

## Memory Review Process

### Daily Review (Heartbeats)

Every few days during a heartbeat:

1. **Load recent daily files**
   ```bash
   # Read last 3-5 days
   read memory/2026-02-18.md
   read memory/2026-02-17.md
   read memory/2026-02-16.md
   ```

2. **Identify significant insights**
   - Important decisions made
   - Lessons learned
   - Patterns discovered
   - Architecture changes

3. **Update MEMORY.md**
   - Add distilled insights
   - Remove outdated info
   - Reorganize if needed

4. **Commit changes**
   ```bash
   git add MEMORY.md
   git commit -m "docs(memory): update long-term memory from recent sessions"
   ```

### Weekly Review

Once per week:

1. **Review error-log.md**
   - Consolidate similar entries
   - Remove obsolete entries (issues resolved)
   - Highlight recurring issues

2. **Clean up daily files**
   - Archive old files (>6 months) to `memory/archive/`
   - Keep recent files accessible
   - Ensure no duplicate entries

3. **Check MEMORY.md**
   - Is it getting too long?
   - Any outdated info?
   - Need to reorganize sections?

---

## Common Patterns

### Pattern 1: Session Start

```markdown
## 14:30 GMT+1 - Session Start

Loaded:
- AGENTS.md
- USER.md
- memory/2026-02-17.md
- memory/2026-02-16.md
- memory/error-log.md

Context: User asked about monitoring setup.
```

### Pattern 2: Task Completion

```markdown
## 15:45 - Deployed Grafana Stack

Task completed successfully.

What was done:
1. Created docker-compose.monitoring.yml
2. Deployed 7 containers
3. Configured Prometheus datasource
4. Created initial dashboards

Result: All services healthy, metrics flowing.

Lessons: cAdvisor configuration needed fixes (see error-log.md)
```

### Pattern 3: Error Discovery

```markdown
## 16:20 - Encountered Error

Error: cAdvisor crashed with "unknown backend storage driver: docker"

Root cause: storage_driver flag not valid.

Fix: Removed flag, restarted container.

Logged to: memory/error-log.md
```

### Pattern 4: User Feedback

```markdown
## 17:00 - User Feedback

User: "The Grafana dashboard needs more CPU metrics"

Action taken:
- Added node_cpu_seconds_total query
- Created CPU usage panel
- Updated dashboard documentation

User response: "Perfect, thanks!"
```

### Pattern 5: Session End

```markdown
## 18:00 - Session Complete

Summary:
- Deployed Grafana monitoring stack
- Fixed cAdvisor configuration issues
- Updated error-log.md with 3 new entries
- Updated documentation

Next steps:
- Add alerting to Grafana
- Migrate remaining Overseer dashboards
- Test alert notifications

Committed: yes
Pushed: yes
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Mental Notes"

**Bad:**
> "I'll remember this for next time" (not written down)

**Good:**
> Write it to a file immediately.

---

### ❌ Anti-Pattern 2: Duplicate Information

**Bad:**
- Same issue in error-log.md, daily file, and MEMORY.md

**Good:**
- error-log.md: What to do differently (concise)
- daily file: What happened (detailed)
- MEMORY.md: Why it matters (curated)

---

### ❌ Anti-Pattern 3: Loading MEMORY.md Everywhere

**Bad:**
> Loading MEMORY.md in Discord group chat

**Why:** Contains personal context that shouldn't leak

**Good:**
> Only load MEMORY.md in main session (direct chats with your human)

---

### ❌ Anti-Pattern 4: Delayed Error Logging

**Bad:**
> "I'll log this error at the end of the session"

**Why:** You'll forget details

**Good:**
> Log to error-log.md IMMEDIATELY

---

### ❌ Anti-Pattern 5: MEMORY.md in Daily Files

**Bad:**
> Putting everything in daily files, never distilling to MEMORY.md

**Why:** MEMORY.md becomes outdated, daily files cluttered

**Good:**
> Distill daily files into MEMORY.md every few days

---

## Memory Maintenance

### Daily Maintenance

1. **At session end:**
   - Write summary to daily file
   - Update error-log.md if needed
   - Commit changes

2. **Before session start:**
   - Read error-log.md
   - Read today + yesterday's daily files
   - Read MEMORY.md (if main session)

### Weekly Maintenance

1. **Review error-log.md:**
   - Consolidate similar entries
   - Remove obsolete entries
   - Highlight recurring issues

2. **Review MEMORY.md:**
   - Update with new insights
   - Remove outdated info
   - Reorganize if needed

3. **Archive old daily files:**
   - Move files >6 months to `memory/archive/`
   - Keep recent files accessible

### Monthly Maintenance

1. **Memory audit:**
   - Check all files are up to date
   - Ensure no duplicates
   - Verify error-log.md is still useful

2. **Cleanup:**
   - Remove test files
   - Delete temporary notes
   - Organize skills documentation

---

## Summary

**Key Takeaways:**

1. **Write It Down** — Files survive session restarts, mental notes don't
2. **Error Log is King** — Log failures immediately, check it every session
3. **Distill, Don't Duplicate** — Daily files (raw), MEMORY.md (curated)
4. **Secure Memory** — MEMORY.md only in main session
5. **Review Regularly** — Update MEMORY.md every few days

**Remember:** The memory system is your continuity across sessions. Use it consistently, and you'll get smarter over time.

---

*Last updated: 2026-02-18*
