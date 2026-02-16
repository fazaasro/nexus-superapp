# Error Log — Auto-Captured Learnings

## Auto-Capture Loop

When ANY of these happen, immediately append to memory/error-log.md:

- A tool call fails or returns unexpected results
- User corrects you ("no, do it this way")
- You discover a gotcha or undocumented behavior
- An assumption you made turns out wrong
- Something takes way longer than expected

Format: - 🏷️ **Short title** — What happened. What to do instead.

## Categories

🔧 **tool-failure** - something broke
🧠 **wrong-assumption** - agent assumed wrong
🔄 **user-correction** - human said "no, do it this way"
💡 **discovery** - learned something useful
⚠️ **gotcha** - undocumented behavior or subtle trap
🏗️ **architecture** - structural decisions worth remembering

---

## 2026-02-16

- ⚠️ **QMD skills collection path** — Using relative path for skills collection matched 0 files. Use absolute path (~/.openclaw/workspace/skills) to index all skill subdirectories.
- 💡 **QMD tsx dependency** — QMD requires tsx locally available. Installed with `bun install -g tsx` then added to workspace with `bun add tsx`.
- 💡 **QMD first-time embedding** — Initial embedding takes 7m on CPU (downloads/builds llama.cpp). Subsequent updates only process new/changed files (fast).
- 💡 **QMD vs native memory_search** — QMD indexes multiple collections (workspace, skills, stack) vs native only searches workspace files. Use QMD for comprehensive search across all knowledge.
- 💡 **QMD search modes** — BM25 (240ms, fast, keyword-based), Vector (2s, semantic but needs AI models), Hybrid (5s, combines both). Use BM25 for 90% of lookups, vector/hybrid for semantic queries.
- ⚠️ **QMD vector search requirements** — vsearch and query modes need llama.cpp compiled locally. First compile takes time, but then runs fast. BM25 mode (search) works immediately without compilation.
- 💡 **Cron job syntax** — Use `--every "1h"` not `--schedule '{"kind":"every","everyMs":3600000}'`. Payload uses `--system-event "text"` for main session.
- 💡 **Cron delivery mechanism** — systemEvent injects text into main session, but agent needs to execute actual command. Combine systemEvent text with explicit command in the text payload.