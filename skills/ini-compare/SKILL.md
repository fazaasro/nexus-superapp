---
name: ini-compare
version: 1.1.0
description: |
  Compare configuration files (INI, YAML, JSON, TOML, etc.) and recommend optimal storage solution.

when_to_use:
  - Comparing configuration formats
  - Analyzing file structures
  - Making recommendations based on use case

when_not_to_use:
  - Just viewing config files (use cat or exec tool directly)
  - For simple edits (use file tools directly)

tools_involved:
  - exec (to read and run commands)
  - file (for direct file operations)

network_policy: none

expected_artifacts:
  - Comparison report (performance metrics, file counts, complexity analysis)
  - Recommendation matrix (which format for which use case)

success_criteria:
  - All formats analyzed and documented
  - Clear winner identified (if applicable)
  - Performance metrics collected
  - Trade-offs documented

---

## Workflows

### compare_formats

Analyze and compare different configuration file formats.

**Supported Formats:**
- INI — Windows/DOS configuration
- JSON — Data interchange, API configs
- YAML — Container orchestration (Docker Compose, OpenClaw)
- TOML — Rust/Cargo configs

**Parameters:**
- `files`: List of config files to compare (e.g., ".env", "docker-compose.yml", "openclaw.json")

**Analysis Criteria:**
- Human-readability (1-5, 1 = best)
- Machine-parsability (1-5, 1 = best)
- Structure (1-5, 1 = best)
- Security (1-5, 1 = best)

**Steps:**
1. Read each file
2. Parse and analyze structure
3. Calculate metrics (lines, nesting depth, complexity)
4. Generate scores
5. Rank formats

**Output:**
```markdown
# Format Comparison Report

## Files Analyzed
- File count: 3

## Metrics Summary

| Format | Human-Readability | Machine-Parsability | Structure | Security | Overall |
|---------|-------------------|-------------------|----------|----------|---------|
| INI | 5 | 4 | 4 | 5 | 18/20 (90%) |
| JSON | 3 | 5 | 5 | 4 | 17/20 (85%) |
| YAML | 5 | 3 | 5 | 4 | 19/20 (95%) |
| TOML | 2 | 4 | 5 | 3 | 18/20 (90%) |

## Ranking
1. YAML (95%) — Best overall
2. INI (90%) — Easy to read
3. JSON (85%) — Flexible, structured
4. TOML (90%) — Rust ecosystem

## Recommendation
**Primary:** Use YAML for container orchestration (Docker Compose, OpenClaw skills)
**Secondary:** Use JSON for data exchange and API configs
**For Humans:** INI for simple environment variables

## Trade-offs

| Format | Pros | Cons |
|---------|------|----------|
| YAML | Human-readable, Docker native | Not as structured as JSON |
| INI | Simple, universal | Limited data types | Can get messy |
| JSON | Structured, flexible | Can be complex | Requires quotes |
| TOML | Rust-native, explicit | Limited ecosystem | Steeper learning curve |

---

### analyze_structure

Analyze a single configuration file for complexity and best practices.

**Parameters:**
- `file`: Path to config file

**Analysis Criteria:**
- Nesting depth (1-5, 1 = best)
- Line count (lower is better)
- Key/Value count (lower is better)
- Comments (clean is better)
- Security (no secrets, proper types)
- Naming conventions

**Scoring:**
1. **Nesting:** 1-5 points
2. **Readability:** 1-5 points
3. **Security:** 1-5 points
4. **Comments:** 1-5 points
5. **Conventions:** 1-5 points

**Rating:**
- Excellent (20-25): Production-ready
- Good (15-19): Well-structured
- Fair (10-14): Some improvements needed
- Poor (0-9): Needs refactoring

**Output:**
```markdown
# File Analysis: docker-compose.yml

## Scores
- Nesting: 3/5 (Shallow nesting, good)
- Readability: 5/5 (Clear structure, good naming)
- Security: 5/5 (No secrets found)
- Comments: 4/5 (Well-documented)
- Conventions: 3/5 (Standard Docker Compose format)

## Overall Rating
**Good (16/25)**

## Recommendations
- Keep environment variables in .env files (not in docker-compose.yml)
- Use YAML anchors for repeated values
- Add comments for complex sections
- Use consistent indentation (2 spaces)
```

---

## Templates

### best_practices

Standard configuration file best practices for different formats.

**INI Best Practices:**
- Section headers in brackets ([Section])
- Key-value pairs: key=value
- Comments start with ; or #
- Use = for boolean values

**JSON Best Practices:**
- Use 2-space indentation
- Use double quotes for keys
- Trailing commas in arrays
- Use null for empty values

**YAML Best Practices:**
- Use 2-space indentation
- Use - for lists
- Use | for key-value pairs
- Use literal | for multiline strings

---

## Guardrails

### Security
- Never expose secrets in config files
- Validate file paths before processing
- Use environment variables for sensitive data

### Performance
- Don't read large files unnecessarily
- Use streaming parsers for huge files
- Cache parsed results if reading multiple times

### Negative Examples

### When NOT to use this skill

- Just viewing a file (use cat or less)
- Making simple edits (use sed or file tools)
- Don't reformat entire files (use targeted edits)

### What to do instead

- For analyzing multiple files (use compare_formats workflow)
- For checking specific key (use grep or file tool)
- For best practices (use best_practices template)

---

## Artifact Locations

All comparison reports go to:
- `workspace/reports/format-analysis/` — Format comparison reports
- `workspace/config/` — Best practices documentation

---

## Version History

- 1.1.0 — Initial release with format comparison workflows
