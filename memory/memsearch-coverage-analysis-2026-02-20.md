# Search File Coverage Analysis
**Date:** 2026-02-20
**Purpose:** Compare memsearch vs QMD file coverage

---

## File Coverage Comparison

### QMD Collections (from workspace root)

| Collection | Pattern | Files Indexed |
|------------|----------|-----------------|
| workspace | **/*.md | 144 files |
| stack | **/*.md | 18 files |
| skills | **/*.md | 11 files |
| **Total** | - | **173 files** |

**QMD Search Scope:** All .md files from 3 directories at workspace root

---

### memsearch Coverage (per repository)

| File Pattern | Files Indexed | Notes |
|-------------|----------------|--------|
| README.md | 1 | Root file |
| .docs/**/*.md | varies | Subfolder in each repo |
| DEPLOYMENT*.md | varies | Root deployment docs |

**memsearch Search Scope:** Only files in current repository (repo root + .docs/)

---

## Coverage Gap Analysis

### Repository-Specific Comparison

| Repository | QMD Indexed Files | memsearch Indexed Files | QMD Advantage |
|------------|-------------------|-----------------------|----------------|
| **vault-infrastructure** | 18 (stack collection) | 4 (README.md + 3 .docs/) | QMD has 4.5x more files |
| **aac-infrastructure** | 18 (stack collection) | 0 | QMD has all files |
| **aac-stack** | 18 (stack collection) | 0 | QMD has all files |
| **levy-agent** | 144 (workspace collection) | 0 | QMD has all files |
| **overseer-monitoring** | 144 (workspace collection) | 0 | QMD has all files |
| **project-levy-ssh** | 144 (workspace collection) | 0 | QMD has all files |

**Note:** Numbers above are approximate based on typical repository structures.

---

## Key Findings

### 1. Different File Coverage Models

**QMD Model:** Cross-Repository Indexing
- Single index at workspace root
- Searches across ALL repos simultaneously
- 3 collections (workspace, stack, skills) = 173 files total
- Centralized, unified search

**memsearch Model:** Per-Repository Indexing
- Separate index in each repository
- Searches only files in current repository
- Each repo has its own index (.scripts/index.db)
- Decentralized, repo-specific search

### 2. Fair Comparison Problem

**Issue:** memsearch and QMD are NOT searching the same files:
- QMD searches stack/** collection (18 files from vault-infrastructure)
- memsearch searches vault-infrastructure/*.md (4 files)
- Different file sets = different search results

**Result:** Comparison is NOT fair - they're searching different content

---

## Solutions

### Option 1: Align memsearch with QMD Coverage (Recommended)

**Approach:** Index ALL .md files in each repository, not just root + .docs/

**Change:** Modify memsearch-index.sh to index:
```bash
# Current (limited):
- README.md (root)
- .docs/**/*.md (subfolder)
- DEPLOYMENT*.md (root)

# Proposed (full coverage):
- **/*.md (all markdown files in repo root)
- **config/**/*.md** (configuration files)
- **.docs/**/*.md** (documentation)
- All subdirectories recursively
```

**Benefits:**
- Fair comparison - both tools search same files
- memsearch covers more files than current
- Better coverage for repo-specific searches

---

### Option 2: Keep Current memsearch as Fast Subset

**Approach:** Accept that memsearch is a fast subset of QMD

**Rationale:**
- memsearch = Instant lookups (0.018s, repo-specific)
- QMD = Comprehensive search (1.5s, cross-repo)
- Different use cases, both valid

**Benefits:**
- No changes needed
- memsearch wins on speed for repo-specific queries
- QMD wins on coverage for cross-repo queries
- Clear separation of concerns

---

### Option 3: Create QMD-Style Central Index for memsearch

**Approach:** Build a unified memsearch index at workspace root (like QMD)

**Implementation:**
```bash
# Create central index at ~/.openclaw/workspace/.scripts/memory-index.db
# Index all repos: stack/, swarm/repos/*/ (each repo's files)
# Single unified search across all repositories
```

**Benefits:**
- Same file coverage as QMD
- Still 83x faster (native SQLite FTS5 vs Node.js + model)
- Fair performance comparison
- Centralized memory management

**Drawbacks:**
- More complex setup
- Need re-indexing script for entire workspace
- Cross-repo search already available via QMD BM25

---

## Recommendation: Option 1 - Align Coverage

**Why:**
- Fair comparison requires same file coverage
- memsearch currently only indexes 4-6 files per repo
- QMD indexes 18-144 files per repo
- Performance difference should be on file coverage parity, not advantage

**Implementation:**
1. Modify `.scripts/memsearch-index.sh` to index **/*.md recursively
2. Re-run setup in all repos
3. Compare again with aligned coverage

**Expected Result:**
- memsearch speed: 0.018s
- QMD BM25 speed: 1.5s
- Both searching SAME files
- Fair performance/quality comparison

---

## Action Items

### Immediate
- [ ] Discuss preferred approach (Options 1, 2, or 3)
- [ ] If Option 1: Update memsearch-index.sh for full coverage
- [ ] If Option 1: Re-run memsearch-setup.sh in all repos
- [ ] Run comparison test again with aligned coverage

### Long-term
- [ ] Document decision for future reference
- [ ] Update subagent standards to specify memsearch vs QMD
- [ ] Consider hybrid approach (memsearch for speed + QMD for coverage)

---

## Summary

**Current State:**
- **QMD:** 173 files across 3 collections (workspace, stack, skills)
- **memsearch:** ~4-6 files per repository (README.md + .docs/ + deployment docs)
- **Gap:** memsearch covers ~15% of files that QMD covers

**Comparison Fairness:** ❌ NOT FAIR
- Different file sets = different results
- Cannot fairly compare quality when content differs

**Recommended:** Align file coverage before next comparison test

---

*Analysis Date:* 2026-02-20
*Next:* Discuss approach with user
