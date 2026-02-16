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