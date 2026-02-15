---
name: storage-wars-2026-skill
version: 1.0.0
description: |
  Complete Storage Wars 2026 benchmarking suite.
  Simulates head-to-head competition between storage backends (Flat Files, SQLite, Qdrant).
  Generates performance reports, rankings, and recommendations.

when_to_use:
  - Running benchmarks to compare storage performance
  - Analyzing benchmark results
  - Generating recommendations for OpenClaw storage stack
  - Creating visual reports and performance charts

when_not_to_use:
  - Just viewing current storage metrics (use monitoring skill)
  - For quick performance checks (use system tool directly)

tools_involved:
  - storage-wars-2026-skill (Main benchmark orchestrator)
  - ini-compare (Compare config formats)
  - performation-benchmark (Run individual performance tests)
  - get_metrics (Fetch current system metrics)

network_policy: none
allowed_domains:
  - zazagaby.online
  - monitor.zazagaby.online

expected_artifacts:
  - Benchmark results (performance metrics)
  - Comparison report (backend analysis)
  - Overall score calculation
  - Ranking tables
  - Recommendation matrix (which backend for which use)
  - Performance visualization (if possible)
  - Optimization recommendations

success_criteria:
  - All benchmarks completed
  - All performance metrics collected
  - Clear winner identified (or trade-offs documented)
  - Recommendation provided
  - Report generated

templates:
  benchmark_report: Standard performance comparison template
  comparison_table: Side-by-side backend comparison
  overall_score: Overall performance scoring
  visual_report: ASCII art/bar charts if enabled

examples:
  - input: "Run full benchmark comparison"
    output: |
      Benchmark Results
      Flat Files: 15200 ops/s (write), 25000 ops/s (read)
      SQLite: 8500 ops/s (write), 5200 ops/s (read)
      Winner: Flat Files (76% faster)
      
  - input: "Compare Flat Files vs SQLite"
    output: |
      Performance Comparison
      Write Speed: Flat Files (15200 ops/s) vs SQLite (8500 ops/s) - 78% faster
      Read Speed: Flat Files (25000 ops/s) vs SQLite (5200 ops/s) - 379% faster
      Overall Score: Flat Files (95/100)

guardrails:
  benchmark_all: Must run 3 iterations before declaring winner
  analyze: Must check 10 quality pillars
  performance_report: Provide detailed analysis
  overall_score: Weighted score across all metrics
  visual_report: Optional ASCII charts for readability
  
negative_examples:
  - Don't run full benchmark on trivial data
  - Don't benchmark without defining success criteria
  - Don't compare different workloads with different test sizes
  
what_to_do_instead:
  - Just check current metrics (use monitoring skill)
  - Use system tools for quick checks (docker ps, df)
  - Compare raw numbers instead of full benchmarks for simple checks

---

## Workflows

### benchmark_suite

Run complete Storage Wars 2026 benchmark suite.

**Parameters:**
- `backends`: Comma-separated list to test (flat-files, sqlite, qdrant)
- `test_size_mb`: Size of test dataset in MB (default: 10)
- `iterations`: Number of benchmark runs (default: 3)

**Steps:**
1. Benchmark write operations on all backends
2. Benchmark read operations on all backends
3. Benchmark search operations on Qdrant (if available)
4. Calculate performance metrics
5. Generate comparison report
6. Determine winner based on weighted score
7. Create visual report (if enabled)

**Metrics:**
- Write Speed: ops/sec (higher is better)
- Read Speed: ops/sec (higher is better)
- Search Latency: ms (lower is better)
- Memory Usage: MB (lower is better)
- Efficiency Score: Weighted performance rating

**Example:**
```bash
# Run full benchmark suite
benchmark_suite backends="flat-files,sqlite,qdrant" test_size_mb=10 iterations=3

# Output:
# Benchmark Results
# Performance Comparison
| Backend | Write | Read | Search | Memory | Score |
|---------|------|------|--------|------|
| Flat Files | 15200 | 25400 | N/A | 5 | 95 |
| SQLite | 8500 | 5200 | 180 | 52.5 | 78.5 |
| Qdrant | 12000 | 15600 | 250 | 150 | 65 |

Winner: Flat Files
```

---

### compare

Compare performance between two storage backends.

**Parameters:**
- `backend1`: First backend to compare
- `backend2`: Second backend to compare
- `metric_type`: write, read, search, memory, or all
- `test_size_mb`: Size of test file for realistic comparison (default: 100)

**Steps:**
1. Get metrics for both backends
2. Calculate delta (improvement %)
3. Generate comparison table

**Example:**
```bash
# Compare Flat Files vs SQLite with 100MB test
compare_backends backend1=flat-files backend2=sqlite test_size_mb=100 metric_type=all

# Output:
# Performance Comparison
| Metric | Flat Files | SQLite | Improvement |
|---------|-----------|--------|------------|
| Write Speed | 15200 ops/s | 8500 ops/s | Flat Files is 79% faster |
| Read Speed | 25400 ops/s | 5200 ops/s | Flat Files is 388% faster |
| Memory Usage | 5 MB | 52.5 MB | Flat Files uses 91% less |

## Recommendation

**Winner:** Flat Files
**Reason:** 388% faster read performance and 91% less memory usage.

```

---

### overall_score

Calculate weighted overall performance score across all metrics.

**Parameters:**
- `metrics_file`: Path to benchmark results
- `backend`: Target backend for analysis
- `weights`: Custom weight values (optional)

**Formula:**
```
score = (write_speed * w_write + read_speed * w_read + memory_usage * w_memory) / count_metrics
```

Where:
- w_write: Write speed weight (default: 30)
- w_read: Read speed weight (default: 25)
- w_memory: Memory weight (default: 20)
- memory_usage: Memory usage weight (inverse, default: 0.1)
- count_metrics: Number of metrics (default: 4)

**Steps:**
1. Read metrics from benchmark results
2. Calculate weighted score
3. Normalize to 0-100 scale

**Example:**
```bash
# Calculate score
overall_score backend=flat-files weights=w_write=30,w_read=25,w_memory=20,memory_usage=0.1

# Output:
Overall Score: 87.3/100
```

---

## Templates

### benchmark_report

Standard benchmark report template with all sections.

```markdown
# Storage Wars 2026 - Performance Report

## Executive Summary
- Overall Score: [score/100]
- Winner: [winning backend]

## Performance Metrics

[metrics_table]

## Rankings

[rankings_table]

## Recommendations

[recommendations_list]

## Winner Analysis

[winner_section]

---

## Guardrails

### Performance
- Don't optimize prematurely
- Use real-world data sizes
- Account for system load

### Accuracy
- Use deterministic benchmarks
- No fudging results

### Fair Comparison
- All backends tested with identical conditions

### Performance
- Realistic test sizes (100MB, not 10MB)
- Account for system load during tests

### Efficiency
- Optimimize for your use case
- Don't use generic recommendations

---

## Artifact Locations

All reports go to:
- `workspace/reports/storage/` — Benchmark reports
- `workspace/config/storage/` — Benchmark configurations

---

## Version History

- 1.0.0 — Initial release
