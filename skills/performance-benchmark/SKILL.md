---
name: performance-benchmark
version: 1.0.0
description: |
  Analyze Storage Wars 2026 benchmark results and generate performance assessment.
  
  Reads benchmark data from storage-wars-2026-skill/SKILL.md.
  Calculates scores, rankings, and provides optimization recommendations.

when_to_use:
  - Running benchmarks (use storage-wars-2026-skill)
  - Analyzing performance results
  - Comparing storage backends
  - Generating performance reports

when_not_to_use:
  - Just viewing raw benchmark data (use exec tool directly)
  - For quick performance checks (use monitoring skill)

tools_involved:
  - exec (to read benchmark files)
  - monitoring-ops (to check system metrics during tests)

network_policy: restricted
allowed_domains:
  - zazagaby.online
  - monitor.zazagaby.online

expected_artifacts:
  - Performance comparison report (write speed, read speed, latency)
  - Overall score calculation
  - Rankings by backend
  - Optimization recommendations
  - Visual insights (if possible)

success_criteria:
  - All benchmarks analyzed
  - Scores calculated and ranked
  - Recommendations provided
  - Report generated

---

## Workflows

### analyze_results

Analyze benchmark results and generate comprehensive performance report.

**Parameters:**
- `backend`: Target backend to analyze (flat, sqlite, qdrant)
- `test_type`: Type of benchmark (write, read, search, all)
- `compare_to`: Compare with another backend

**Steps:**
1. Read benchmark results from `storage-wars-2026-skill/SKILL.md`
2. Calculate performance metrics for target backend
3. Compare with other backend if specified
4. Calculate overall score
5. Generate rankings
6. Provide recommendations

**Performance Metrics:**
- **Write Speed:** Operations per second (ops/s)
- **Read Speed:** Operations per second (ops/s)
- **Search Latency:** Response time in milliseconds (ms)
- **Memory Usage:** Memory footprint in MB
- **Efficiency Score:** Weighted score (write * 2 + read / latency factor)

**Example:**
```bash
# Analyze SQLite performance
analyze_results backend=sqlite test_type=read

# Output:
# Performance Analysis: SQLite
- Write Speed: 8500 ops/s
- Read Speed: 5200 ops/s
- Search Latency: 180 ms
- Efficiency Score: 78.5 (good)
```

---

### compare_backends

Compare performance metrics between two storage backends.

**Parameters:**
- `backend1`: First backend (e.g., flat files)
- `backend2`: Second backend (e.g., sqlite, qdrant)
- `metric_type`: Which metric to compare (write, read, search, latency, memory, efficiency)
- `weight_file`: Path to metric weights file (default)

**Steps:**
1. Get metrics for both backends
2. Calculate delta (improvement %)
3. Determine winner (better score)
4. Generate comparison table

**Performance Metrics:**
| Metric | Backend 1 | Backend 2 | Winner |
|---------|-----------|-----------|----------|--------|
| Write Speed | value1 ops/s | value2 ops/s | % faster |
| Read Speed | value3 ops/s | value4 ops/s | % faster |
| Search Latency | value1 ms | value2 ms | % faster |
| Memory Usage | value1 MB | value2 MB | % lower |

**Example:**
```bash
# Compare Flat Files vs SQLite
compare_backends backend1=flat backend2=sqlite metric_type=write
```

---

### overall_score

Calculate overall performance score across all backends and benchmarks.

**Parameters:**
- `backends`: Comma-separated list of backends
- `weights_file`: Path to metric weights (default: internal)

**Formula:**
```
score = (write_speed * w_write + read_speed * w_read + 
        (1/latency) * w_latency + 
        (1/memory) * w_memory) * w_memory_rev +
        (1/efficiency) * w_efficiency) * w_efficiency_rev) / 
        count_metrics) / (1 + len(weights))

Where:
- w_write = write speed weight
- w_read = read speed weight
- w_latency = (1/latency) weight (lower is better)
- w_memory = (1/memory) weight (lower is better)
- w_memory_rev = (1/memory) weight
- w_efficiency = efficiency score weight
- w_efficiency_rev = (1 - efficiency_score) weight
- count_metrics = number of metrics to average

**Output:**
```markdown
# Overall Performance Score

## Backend Rankings

| Backend | Write (ops/s) | Read (ops/s) | Latency (ms) | Memory (MB) | Efficiency | Overall |
|-----------|---------------|---------------|----------|----------|----------|----------|
| Flat Files | 15200 | 25400 | N/A | 5 | 82 | 85 |
| SQLite | 8500 | 5200 | 180 | 45 | 78.5 |
| Qdrant | 12500 | 15600 | 220 | 120 | 65 | 75 |

**Winner:** Flat Files (Score: 85)
```

---

### get_metrics

Fetch current system metrics for performance assessment.

**Parameters:**
- `backend`: Target backend to check (optional)

**Steps:**
1. Read current system metrics (CPU, RAM, Disk, Network)
2. Check for resource bottlenecks
3. Identify performance degradation

**Example:**
```bash
# Check SQLite backend performance
get_metrics backend=sqlite

# Output:
# Current System Metrics
- CPU: 25%
- RAM: 45%
- Disk: 62%
- SQLite Performance: 78.5 (from benchmark)
```

---

## Visual Report

Generate visual performance charts and graphs from benchmark data.

**Parameters:**
- `backend`: Target backend for report
- `chart_type`: Type of chart (bar, line, scatter)
- `format`: Output format (markdown, html)

**Charts Available:**
- Write Speed Comparison (bar chart)
- Read Speed Comparison (bar chart)
- Latency Comparison (line chart)
- Memory Usage Comparison (bar chart)
- Efficiency Trend (line chart)

**Example:**
```bash
# Generate performance visualization
visual_report backend=sqlite chart_type=bar

# Output: (Markdown chart)
## Write Speed by Backend
```ascii
Flat Files | ████░░░ (15200 ops/s)
SQLite      | ███░░░░ (8500 ops/s)
Qdrant      | ████░░░ (12500 ops/s)
```

---

## Templates

### performance_report

Standard performance comparison report template.

```markdown
# Performance Report
**Date:** [current timestamp]

## Executive Summary
- Overall Performance Score: [score/100]
- Winner: [winning backend]
- Bottlenecks: [list of issues]

## Detailed Metrics
### Write Performance
[metrics_table]

### Read Performance
[metrics_table]

### Search Performance
[metrics_table]

### Memory Usage
[metrics_table]

### Efficiency Score
[calculation]

### Recommendations
[list of improvements]

## Trade-offs
[analysis]

---

## Guardrails

### Performance Expectations
- Actual performance varies by hardware
- Benchmark results are for reference only
- Don't make production decisions based on single benchmarks

### Fair Comparison
- All backends tested under similar conditions
- Account for system load during tests

### Accuracy
- Benchmark scripts must be deterministic
- No fudging results to favor any backend
- Document test methodology

---

## Artifact Locations

All reports go to:
- `workspace/reports/performance-reports/` — Performance comparison reports
- `workspace/config/` — Metric weights and thresholds

---

## Version History

- 1.0.0 — Initial release with Storage Wars 2026 benchmarking
