# 2026-02-10 — GLM Model Added to OpenClaw

## Task
Add GLM model to OpenClaw and set as main model. Use Kimi K2.5 only for coding tasks via kimi-cli.

## Changes Made

### OpenClaw Configuration (`/home/ai-dev/.openclaw/openclaw.json`)

**Before:**
```json
{
  "primary": "kimi-coding/k2p5",
  "models": {
    "kimi-coding/k2p5": {"alias": "Kimi K2.5"}
  }
}
```

**After:**
```json
{
  "auth": {
    "profiles": {
      "glm:default": {"provider": "glm", "mode": "api_key"},
      "kimi-coding:default": {"provider": "kimi-coding", "mode": "api_key"},
      "zai:default": {"provider": "zai", "mode": "api_key"}
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-4.7"
      },
      "models": {
        "glm": {"alias": "GLM-4-Plus (Main)"},
        "kimi-coding/k2p5": {"alias": "Kimi K2.5 (Coding Backup)"},
        "zai/glm-4.7": {...}
      }
    }
  }
}
```

### Status
- **OpenClaw Gateway:** Running (PID 178917)
- **Primary Model:** zai/glm-4.7 (GLM-4-Plus)
- **Coding Backup:** kimi-coding/k2p5 (Kimi K2.5)

### API Key
- GLM API Key: `44ccf5decb22442e94be7e6271f84e47.eNJl2NFWKFOTaP8W`
- Added to `glm:default` profile

### Usage Strategy
- **Default (GLM-4-Plus):** General tasks, reasoning, analysis
- **Coding (Kimi K2.5):** Use via `kimi-cli` when specifically needed for coding tasks

---

*Task completed: GLM model configured as primary in OpenClaw*
