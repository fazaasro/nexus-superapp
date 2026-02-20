# memsearch vs QMD - Fair Comparison Test
**Date:** 2026-02-20
**Status:** All 6 repos added to QMD, first fair comparison completed

---

## Setup Changes

### Added QMD Collections

| Collection | Path | Files | Status |
|------------|------|-------|--------|
| **vault-repo** | ~/swarm/repos/vault-infrastructure | 5 | ✅ Added |
| **aac-infra** | ~/swarm/repos/aac-infrastructure | 4 | ✅ Added |
| **aac-stack** | ~/swarm/repos/aac-stack | 5 | ✅ Added |
| **levy-agent** | ~/swarm/repos/levy-agent | 4 | ✅ Added |
| **overseer** | ~/swarm/repos/overseer-monitoring | 0 | ✅ Added |
| **levy-ssh** | ~/swarm/repos/project-levy-ssh | 3 | ✅ Added |

**Total QMD Collections:** 9 (was 3)
**Total Files Indexed:** 194 (was 173)
**Files Added:** 21 new files from 4 repositories

---

## Fair Comparison Test: "vault deployment"

### memsearch Results (vault-infrastructure)

**System:** Python memsearch (SQLite FTS5)
**Files Indexed:** 5 (vault-repo: README.md, VAULT_SETUP.md, DEPLOYMENT_SUMMARY.md, POST_DEPLOYMENT_CHECKLIST.md, README-MEMSEARCH.md)
**Search Time:** 0.019s

**Results:**
```
1. DEPLOYMENT_SUMMARY.md
   Title: Vault Deployment Summary
   Score: N/A
   Content: # Vault Deployment Summary
   - Completed tasks: Deploy Vault using Docker Compose
   - Container: vault (hashicorp/vault:latest)
   - Port: 127.0.0.1:8200
   - File: 6.8 KB

2. POST_DEPLOYMENT_CHECKLIST.md
   Title: Post-Deployment Checklist
   Score: N/A
   Content: Complete these steps to finalize Vault deployment
   - Section 1: Cloudflare DNS Configuration
   - Section 2: Access App Configuration
   - Section 3: Token Configuration
```

**Quality:** Good
- ✅ Found 2/5 relevant files (40% of indexed files)
- ✅ Content directly relevant to query
- ✅ Fast results (0.019s)

### QMD BM25 Results (vault-repo collection)

**System:** QMD BM25 on vault-repo collection
**Files Indexed:** 5 (same files as memsearch!)
**Search Time:** 2.326s

**Results:**
```
1. qmd://vault-repo/deployment-summary.md:1
   Title: Vault Deployment Summary
   Score: 86%
   @@ -1,3 @@ (0 before, 229 after)
   
2. qmd://vault-repo/post-deployment-checklist.md:3
   Title: Post-Deployment Checklist
   Score: 86%
   @@ -2,4 @@ (1 before, 213 after)
   
   Complete these steps to finalize Vault deployment.
   ## Section 1: Cloudflare DNS Configuration
```

**Quality:** Excellent
- ✅ Found 2/5 relevant files (40% of indexed files)
- ✅ Same files as memsearch (FAIR COMPARISON!)
- ✅ Better context with line numbers (@@ references)
- ✅ Higher relevance scores (86%)
- ✅ Markdown code blocks preserved

---

## Performance Comparison (FAIR)

| Metric | memsearch | QMD BM25 | Difference |
|--------|-----------|-----------|------------|
| **Files Indexed** | 5 | 5 | ✅ **SAME** |
| **Search Time** | 0.019s | 2.326s | memsearch 122x faster |
| **Results Found** | 2 relevant | 2 relevant | ✅ **TIE** |
| **Relevance Score** | N/A (basic rank) | 86% (advanced BM25) | 🏆 **QMD** |
| **Context Quality** | Raw content | Line numbers + code blocks | 🏆 **QMD** |
| **Coverage** | Repo-only | Repo-only | ✅ **TIE** |

---

## Analysis

### Results: **TIE** (2/2 files found)
Both tools found the same 2 files out of 5:
- DEPLOYMENT_SUMMARY.md (or deployment-summary.md)
- POST_DEPLOYMENT_CHECKLIST.md (or post-deployment-checklist.md)

### memsearch Strengths
- 🏆 **Speed:** 122x faster (0.019s vs 2.326s)
- ✅ Instant feedback for interactive debugging
- ✅ Simple, no external dependencies

### QMD BM25 Strengths
- 🏆 **Context Quality:** Line numbers, code blocks
- 🏆 **Relevance Scoring:** 86% vs basic ranking
- 🏆 **Markdown Formatting:** Preserves structure
- 🏆 **Cross-Repo Search:** Can search all 9 collections at once

---

## Use Case Recommendations

| Scenario | Recommended Tool | Why |
|----------|------------------|-----|
| **Repo-specific queries** | **memsearch** | 122x faster, instant feedback |
| **Interactive debugging** | **memsearch** | 10 searches = 0.19s vs 23.3s (23s saved) |
| **Code/context needed** | **QMD BM25** | Line numbers, code blocks, 86% scores |
| **Cross-repo search** | **QMD BM25** | Search all 9 collections (194 files) |
| **Quick lookup** | **memsearch** | 0.019s is instant |

---

## Decision Matrix

| Priority | Use memsearch | Use QMD BM25 | Rationale |
|----------|----------------|----------------|-----------|
| **Speed critical** | ✅ Yes | ❌ No | Interactive debugging, high-frequency |
| **Context needed** | ❌ No | ✅ Yes | Code blocks, line numbers |
| **Cross-repo** | ❌ No | ✅ Yes | QMD searches 194 vs 5 files |
| **Relevance matters** | ❌ No | ✅ Yes | QMD's 86% scores vs basic rank |
| **Repo-specific** | ✅ Yes | ❌ Yes | memsearch indexes current repo only |

---

## Updated Statistics

### QMD Collections

| Collection | Path | Files | Last Updated |
|------------|------|-------|--------------|
| workspace | ~/.openclaw/workspace | 144 | 12h ago |
| stack | ~/stack | 18 | 9d ago |
| skills | ~/.openclaw/workspace/skills | 11 | 4d ago |
| vault-repo | ~/swarm/repos/vault-infrastructure | 5 | 34m ago |
| aac-infra | ~/swarm/repos/aac-infrastructure | 4 | 14h ago |
| aac-stack | ~/swarm/repos/aac-stack | 5 | 7d ago |
| levy-agent | ~/swarm/repos/levy-agent | 4 | 7d ago |
| overseer | ~/swarm/repos/overseer-monitoring | 0 | never |
| levy-ssh | ~/swarm/repos/project-levy-ssh | 3 | 7d ago |

**Total:** 9 collections, 194 files

### memsearch Deployment

**Repositories with memsearch:**
- ✅ vault-infrastructure (5 files, Python script)
- ✅ aac-infrastructure (0 files, ready to index)
- ✅ aac-stack (0 files, ready to index)
- ✅ levy-agent (0 files, ready to index)
- ✅ overseer-monitoring (0 files, ready to index)
- ✅ project-levy-ssh (0 files, ready to index)

**Setup per repo:**
```bash
# One-time setup
./.scripts/memsearch-setup.sh  # Creates DB, indexes files

# Re-index
python3 .scripts/memsearch-index.py

# Search
./.scripts/memsearch-search.sh "query" [limit]
```

---

## Final Decision

**Both tools are useful for different use cases.**

### memsearch Use Cases
- ✅ Interactive debugging (122x faster)
- ✅ High-frequency searches (10+ queries)
- ✅ Repo-specific lookups
- ✅ Building scripts with many searches

### QMD BM25 Use Cases
- ✅ Code/context needed (line numbers, blocks)
- ✅ Cross-repo searches (9 collections, 194 files)
- ✅ Better relevance required (86% scores)
- ✅ AI assistant queries (most cases)

### Summary

| Aspect | memsearch | QMD BM25 |
|--------|-----------|-----------|
| **Speed** | 🏆 122x faster | 2.3s |
| **Relevance** | Basic | 🏆 Advanced (86%) |
| **Context** | Raw | 🏆 Rich (line numbers) |
| **Coverage** | Repo-only | 🏆 Cross-repo (194 files) |

**Recommendation:** Use memsearch for speed-critical workflows. Use QMD BM25 for everything else (relevance, context, cross-repo).

---

## Files Created/Updated

- `memory/memsearch-vs-qmd-test-2026-02-20.md` - This file
- All 6 repos added to QMD collections
- Fair comparison completed with same file coverage

---

## Action Items

- [ ] Run memsearch setup in remaining 5 repos (aac-infrastructure, aac-stack, levy-agent, overseer-monitoring, project-levy-ssh)
- [ ] Document final decision in MEMORY.md
- [ ] Update README-MEMSEARCH.md with new QMD collections
- [ ] Commit and push changes

---

*Test Date:* 2026-02-20*
*Status:* Fair comparison complete - both tools now indexing same files*
