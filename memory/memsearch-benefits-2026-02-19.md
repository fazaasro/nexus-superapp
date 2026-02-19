# memsearch vs QMD - Practical Speed Benefits
**Date:** 2026-02-19
**Focus:** When does 0.018s vs 1.5s actually matter?

## Executive Summary

**Answer: Only in specific scenarios.** For most AI assistant use cases, 1.5s is acceptable. The 83x speed advantage matters primarily in **high-frequency, interactive workflows** where you search repeatedly.

---

## Speed Comparison

| Metric | memsearch | QMD BM25 | Difference |
|--------|-----------|-----------|------------|
| **Single Search** | 0.018s | 1.5s | 83x faster |
| **10 Searches** | 0.18s | 15s | 14.8s saved |
| **20 Searches** | 0.36s | 30s | 29.6s saved |
| **50 Searches** | 0.90s | 75s | 74.1s saved |

**Perception:**
- **memsearch:** Instant (18ms = human blink threshold)
- **QMD BM25:** Noticeable delay (1500ms = feels like "thinking")

---

## Real-World Scenarios Where Speed Matters

### 1. Interactive CLI Workflows 🎯 PRIMARY BENEFIT

**Scenario:** Developer debugging issue, searching for API commands, error messages

**Workflow:**
```bash
# Search for error
memsearch "Unable to authenticate" 3  # instant

# Quick read, search again
memsearch "X-Auth-Key" 2  # instant

# Another lookup
memsearch "bearer token" 3  # instant
```

**Why memsearch wins:**
- **Instant feedback loop** - no waiting between searches
- **Flow state maintained** - not disrupted by 1.5s pauses
- **Natural exploration** - quick refinement of queries

**With QMD:**
- Each search breaks flow (1.5s pause)
- 20 searches = 30 seconds of waiting
- Mental reset between searches

---

### 2. Shell Functions & Aliases

**Scenario:** Custom shell command that searches memory as part of workflow

**Example:**
```bash
# Custom command to check API usage
check_api() {
  echo "Cloudflare API usage:"
  memsearch "Cloudflare API" 1
  echo ""
  echo "GitHub API usage:"
  memsearch "GitHub API" 1
}

# Runs instantly
check_api
```

**With memsearch:** Command feels native/instant
**With QMD:** 3s delay makes command feel sluggish

---

### 3. Batch Search Scripts

**Scenario:** Script that searches for multiple patterns across memory

**Example:**
```bash
#!/bin/bash
# Check all security-related entries
for term in "ssh key" "password" "token" "secret"; do
  echo "=== $term ==="
  memsearch "$term" 2
done
```

**Performance:**
- **memsearch:** 0.072s (4 searches × 0.018s)
- **QMD:** 6.0s (4 searches × 1.5s)
- **Time saved:** 5.9s (83x faster)

**Use Case:** Security audits, documentation review, pattern searches

---

### 4. Developer Autocomplete/Integration

**Scenario:** Editor plugin or IDE integration that searches memory

**Requirements:**
- Must be instant (<100ms) for autocomplete
- Users type fast, need instant feedback

**memsearch:** ✅ Meets requirement (18ms)
**QMD:** ❌ Too slow (1500ms) - breaks autocomplete flow

---

### 5. Debugging Sessions (High Frequency)

**Scenario:** Investigating complex issue, need to reference past decisions

**Workflow:**
1. Search: "tunnel setup" → read result
2. Search: "dns records" → read result
3. Search: "access policy" → read result
4. Search: "error 522" → read result
5. ... (repeat 20 times)

**Time breakdown:**
```
memsearch: 20 × 0.018s = 0.36s (instant)
QMD:      20 × 1.5s   = 30.0s (noticable)
```

**Impact:**
- **memsearch:** Seamless investigation, maintain flow
- **QMD:** 30 seconds of waiting, breaks focus

---

## When Speed DOESN'T Matter

### 1. AI Assistant Responses (Most Use Cases)

**Scenario:** You ask me a question, I search memory

**Analysis:**
- My response generation: 2-5 seconds
- Search time (memsearch): 0.018s (negligible)
- Search time (QMD): 1.5s (small fraction of total)

**Conclusion:** Both are fine. 1.5s doesn't noticeably affect total response time.

---

### 2. Occasional Lookups

**Scenario:** Check something once per session

**Example:** "What was the Vault tunnel ID?"

**Impact:**
- **memsearch:** Instant gratification
- **QMD:** 1.5s wait (acceptable for occasional use)

**Conclusion:** User won't notice difference for single searches.

---

### 3. Research Mode (Reading Results Takes Time)

**Scenario:** Search for docs, read through results for 5 minutes

**Analysis:**
- Search time: 1.5s (QMD) vs 0.018s (memsearch)
- Reading time: 300 seconds
- Search as % of total: 0.5% vs 0.006%

**Conclusion:** Irrelevant difference when you're reading for minutes.

---

## Resource Usage Benefits

### CPU & Memory

| Metric | memsearch | QMD BM25 |
|--------|-----------|-----------|
| **Process** | sqlite3 (native) | node + qmd (JS) |
| **Startup time** | 0s (always ready) | ~0.5s (node startup) |
| **Memory footprint** | ~5MB (DB) | ~100MB (Node + model) |
| **CPU usage** | Minimal | Higher (Node runtime) |

**Impact:**
- **memsearch:** Lightweight, always responsive
- **QMD:** Heavier, can delay other operations

---

## Latency Perception (Human Factors)

### Response Time Categories

| Time | Perception | Example |
|-------|-----------|---------|
| **<100ms** | Instant | Click, no delay |
| **100-300ms** | Slight delay | Page load (acceptable) |
| **300-1000ms** | Noticeable | Form submission |
| **>1000ms** | Waiting | Loading spinner |

### Where Each Falls

- **memsearch (18ms):** Instant ✅ (below human perception threshold)
- **QMD (1500ms):** Noticeable delay ⏳ (feels like "thinking")

**Psychological impact:**
- **Instant tools** feel native, integrated
- **Delayed tools** feel like separate service/external
- **Flow breaking** happens >500ms in interactive work

---

## Practical Benefits Summary

### memsearch Benefits
1. ✅ **Instant feedback** - Maintains flow state
2. ✅ **Interactive exploration** - Quick query refinement
3. ✅ **High-frequency workflows** - Batch searches, scripts
4. ✅ **Developer tools** - Autocomplete, IDE integration
5. ✅ **Lightweight** - Low CPU/memory usage
6. ✅ **Always ready** - No startup time

### QMD BM25 Benefits
1. ✅ **Better relevance** - 0-100% scoring, higher accuracy
2. ✅ **Cross-collection** - workspace + stack + skills
3. ✅ **Context awareness** - Snippets, line numbers
4. ✅ **Acceptable speed** - 1.5s fine for occasional use
5. ✅ **Advanced features** - More query options

---

## Decision Framework

### Use memsearch when:
- ✅ Searching repeatedly in a session (10+ searches)
- ✅ Building interactive tools/aliases
- ✅ Batch searching (scripts, audits)
- ✅ Need instant feedback
- ✅ Resource-constrained environment

### Use QMD BM25 when:
- ✅ Single search per query (most AI assistant use)
- ✅ Need high relevance scores
- ✅ Cross-collection search required
- ✅ Reading results takes time anyway
- ✅ Speed not critical

---

## Real-World Example: Debugging Session

**Scenario:** Investigating Cloudflare Tunnel issues

**With memsearch:**
```bash
# 20 searches over 10 minutes
Total search time: 0.36s (instant)
Result: Seamless investigation, flow maintained
```

**With QMD:**
```bash
# 20 searches over 10 minutes
Total search time: 30s
Result: 30 seconds of waiting, 5% of investigation time lost to delay
```

**Impact:** Not critical for one session, but adds up over time.

---

## Bottom Line

**Speed matters when:**
- You're searching repeatedly (10+ times)
- Building interactive tools
- Doing batch operations
- Need instant feedback (sub-100ms)

**Speed doesn't matter when:**
- Single search per query (most AI assistant use)
- Reading results takes time
- Research mode (minutes of reading)

**Answer:** memsearch's speed advantage is **real but niche**. For 90% of AI assistant use cases, 1.5s is perfectly fine. The 83x speedup only matters in specific high-frequency, interactive workflows.

**Practical recommendation:**
- Default: QMD BM25 (better relevance, acceptable speed)
- Interactive debugging: memsearch (instant, maintain flow)
- Batch scripts: memsearch (83x faster)
- Single lookup: Either (1.5s vs 0.018s, both fine)

---

*Generated: 2026-02-19*
*Session: memsearch Benefits Analysis*
