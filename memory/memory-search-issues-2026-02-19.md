# Memory Search Investigation - 2026-02-19
**Date:** 2026-02-19
**Issue:** Native memory_search returning empty results

## Problem Discovery

Testing native `memory_search` tool revealed it's **not working**:

```bash
memory_search({"query": "vault cloudflare", "maxResults": 3})
# Returns: {"results": [], "provider": "none", "mode": "fts-only"}
```

**Status:**
- Provider: `none` (no search backend configured)
- Mode: `fts-only` (full-text search only)
- Results: Empty array (no files indexed)

## Files Available

| File | Lines | Content |
|------|-------|---------|
| MEMORY.md | 734 | Long-term curated memory |
| memory/error-log.md | 81 | Error log and learnings |
| memory/*.md | 42 files | Daily logs, session summaries |

**Total searchable content:** ~815+ lines across 43 files

## Root Cause Analysis

### 1. No Search Provider
`"provider": "none"` indicates:
- No FTS engine (SQLite FTS5, Meilisearch, etc.) configured
- No vector search backend (Qdrant, Pinecone, etc.) configured
- Tool is likely doing linear file scanning (slow)

### 2. No Index
Without a provider:
- Every search scans all files linearly
- No pre-built index to speed up queries
- Should still return results, but doesn't

### 3. Configuration Missing
Tool appears to need:
- FTS backend configuration
- Index path specification
- Collection setup (similar to QMD)

## Comparison: Native vs QMD

| Aspect | Native memory_search | QMD BM25 |
|--------|---------------------|-----------|
| **Status** | ❌ Broken (no results) | ✅ Working (1.3s) |
| **Provider** | None (not configured) | SQLite FTS5 |
| **Index** | None | 169 files indexed |
| **Speed** | Unknown (broken) | 1.3 seconds |
| **Coverage** | Workspace only | Workspace + stack + skills |
| **Relevance** | N/A | 86% for tech queries |

---

## How to Make Native memory_search Faster

### Option 1: Configure FTS Backend (Recommended)

**SQLite FTS5 Setup:**
```bash
# Create FTS5 virtual table
sqlite3 ~/.cache/memory-search/index.db << 'EOF'
CREATE VIRTUAL TABLE documents USING fts5(
  title,
  content,
  path,
  tokenize='porter unicode61'
);
EOF

# Index all memory files
for file in ~/.openclaw/workspace/memory/*.md ~/.openclaw/workspace/MEMORY.md; do
  # Insert into FTS table
  # ... indexing logic
done
```

**Benefits:**
- Millisecond search speeds
- Full-text search with ranking
- Low memory footprint
- No external dependencies

### Option 2: Use QMD as Memory Backend

**Integration:**
```bash
# Add memory/ as a QMD collection
qmd collection add ~/.openclaw/workspace/memory --name memory --pattern "**/*.md"

# Search memory via QMD
qmd search "query" -c memory
```

**Benefits:**
- Already working (1.3s)
- Familiar interface
- Cross-collection support
- Index already exists

### Option 3: Vector Search with Local LLM

**Setup:**
```bash
# Use existing QMD vector search
qmd vsearch "semantic query" -c memory
```

**Benefits:**
- Semantic understanding
- Synonym matching
- Better for "how to" queries

**Drawbacks:**
- Slow on CPU (99s)
- Requires GPU for speed

---

## Real Use Cases for QMD

### 1. Cross-Collection Documentation Search ✅ PRIMARY USE CASE

**Scenario:** Building a new skill, need to reference existing patterns

**Query:**
```bash
qmd search "docker compose ports 127.0.0.1" -n 5
```

**Why QMD:**
- Searches workspace (current work) + stack (infrastructure configs) + skills (documentation)
- Finds docker-compose.yml examples across all knowledge bases
- BM25 fast enough for technical terms

**Example Result:**
```
qmd://stack/docker-compose.yml:45
Score: 91%
ports:
  - "127.0.0.1:9000:9000"  # Cloudflare tunnel security
```

---

### 2. Skill Pattern Discovery

**Scenario:** Implementing new skill, need to see how other skills handle CLI tools

**Query:**
```bash
qmd search "when_to_use:" -c skills -n 10
```

**Why QMD:**
- Native memory_search doesn't index skills/
- QMD has all 11 skills indexed
- Fast BM25 search across skill files

**Use Case:** Finding skill development patterns, CLI usage, error handling approaches

---

### 3. Infrastructure Configuration Reference

**Scenario:** Debugging service connection, need to find all references to a port

**Query:**
```bash
qmd search ":8200" -c stack -n 5
```

**Why QMD:**
- Searches all stack/ configs (docker-compose, .env files)
- Finds Vault service config, Cloudflare tunnel config
- Technical term matching (exact port numbers)

**Example Result:**
```
qmd://stack/vault/docker-compose.yml:12
Score: 88%
ports:
  - "127.0.0.1:8200:8200"
```

---

### 4. API Command Lookup

**Scenario:** Need exact Cloudflare API command used in previous work

**Query:**
```bash
qmd search "X-Auth-Key header" -n 3
```

**Why QMD:**
- Exact string matching (BM25 excels here)
- Finds code examples, CLI commands, API calls
- Fast (<2 seconds)

**Example Result:**
```
qmd://workspace/memory/error-log.md:29
Score: 86%
Solution: Use "X-Auth-Email: <email>" and "X-Auth-Key: <token>" headers
```

---

### 5. Troubleshooting Error Messages

**Scenario:** Seeing an error, want to find if it's been documented before

**Query:**
```bash
qmd search "Unable to authenticate request" -n 5
```

**Why QMD:**
- Searches error-log.md + daily logs + session summaries
- Finds root cause and solutions
- Technical error message matching

---

### 6. Decision History Reference

**Scenario:** Why did we choose Cloudflare Tunnel over nginx?

**Query:**
```bash
qmd search "tunnel nginx comparison" -n 3
```

**Why QMD:**
- Searches MEMORY.md (long-term decisions)
- Finds architecture decisions with rationale
- Context from multiple files

**Example Result:**
```
qmd://workspace/MEMORY.md:128
Score: 82%
Infrastructure (2026-02-08):
- Cloudflare Tunnel + Access is the correct stack for zero-trust
```

---

## When to Use Which Search

### Native memory_search (If Fixed)
- ✅ Workspace-only queries (fastest potential)
- ✅ Recent memory lookups (today, yesterday)
- ✅ Quick fact checking from MEMORY.md
- ❌ **Currently broken - returns no results**

### QMD BM25 (`qmd search`)
- ✅ **Cross-collection search** (workspace + stack + skills)
- ✅ Technical queries (API commands, file paths, ports)
- ✅ Documentation lookup (skills, architecture)
- ✅ Error message troubleshooting
- ✅ Decision history (MEMORY.md)
- ⏳ Fast enough for daily use (1-2s)

### QMD Vector (`qmd vsearch`)
- ✅ Conceptual questions ("how does X work?")
- ✅ Synonym-based queries (finds related concepts)
- ✅ Deep semantic understanding
- ❌ **Too slow on CPU** (99s)
- ⏳ Use only on GPU or with significant time budget

---

## Recommendations

### Immediate Actions
1. ✅ **Use QMD BM25** as primary search tool (native tool broken)
2. ✅ **Add memory/ as QMD collection** for workspace-only fast searches
3. ⏳ **Fix native memory_search** by configuring FTS backend (longer term)

### Short-Term Workflows
```bash
# Cross-collection search (use QMD)
qmd search "docker ports 127.0.0.1" -n 5

# Memory-only search (add as collection)
qmd collection add ~/.openclaw/workspace/memory --name memory --pattern "**/*.md"
qmd search "vault api key" -c memory -n 5

# Vector search (rare, slow)
qmd vsearch "how does cloudflare access work" -n 3
```

### Long-Term Goals
1. Configure SQLite FTS5 for native memory_search
2. Setup automatic indexing via cron
3. Consider GPU for vector search acceleration
4. Create search aliases for common queries

---

## Summary

**Native memory_search is currently broken** (returns empty results, no provider configured). Until fixed:

**Use QMD BM25 for:**
- All cross-collection searches (workspace + stack + skills)
- Technical queries with exact terms
- Fast daily lookups (1-2 seconds)

**QMD shines for:**
1. Cross-collection documentation search
2. Skill pattern discovery
3. Infrastructure configuration reference
4. API command lookup
5. Troubleshooting error messages
6. Decision history reference

**QMD BM25 is now the primary search tool** until native memory_search is configured with a proper FTS backend.

---

*Generated: 2026-02-19*
*Session: Memory Search Investigation*
