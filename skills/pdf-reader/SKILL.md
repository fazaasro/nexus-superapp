---
name: pdf-reader
version: 1.0.0
description: |
  Read and analyze PDF files for skill development.
  
when_to_use:
  - Reading skill PDFs or documentation
  - Analyzing PDF content for skill creation

when_not_to_use:
  - Reading binary files (images, executables)
  - For simple text viewing, use cat or less

tools_involved:
  - cat (for text files)
  - pdftotext (for PDF content)
  - file (for metadata)

network_policy: none

expected_artifacts:
  - Extracted text/content from PDF
  - File metadata (size, type, pages)
  - Analysis of PDF content

success_criteria:
  - PDF file exists and is readable
  - Content successfully extracted
  - Analysis completed

---

## Workflows

### read_pdf

Read a PDF file and extract text content.

**Parameters:**
- `file`: Path to PDF file

**Steps:**
1. Check if file exists
2. Extract text using pdftotext
3. Analyze content
4. Generate report

**Example:**
```bash
# Read Storage Wars 2026 PDF
read_pdf /home/ai-dev/swarm/repos/storage-wars-2026/README.md
```

---

### analyze_pdf

Analyze extracted PDF content and provide insights.

**Parameters:**
- `content`: Extracted PDF text or content

**Analysis:**
- Count pages
- Identify topics
- Extract key information
- Summarize findings

**Example:**
```bash
# Analyze skill documentation
analyze_pdf content="# Storage Wars 2026 Guide"
analysis="Comprehensive guide covering skills, benchmarks, and recommendations"
```

---

## Templates

### skill_guide_analysis

Analysis template for skill documentation.

```markdown
# Skill Analysis: [skill_name]

## Content Overview
[content_overview]

## Structure Analysis
[structure_analysis]

## Quality Assessment
[quality_assessment]

## Recommendations
[recommendations]

## File Metadata
[metadata]

---

## Guardrails

### File Safety
- Only read PDFs (don't execute)
- Don't process binary files
- Verify file is a PDF before reading

### Accuracy
- Extract all text accurately
- Count pages correctly
- Don't hallucinate content

---

## Negative Examples

### When NOT to use this skill

- Don't use read_pdf on binary files (use file tool instead)
- Don't use read_pdf on non-PDF files (use cat instead)
- For simple viewing (less than 1 page), don't run full PDF analysis

### What to do instead

```
# Don't run full PDF extraction
cat /path/to/file.pdf | head -20

# View PDF metadata
file /path/to/file.pdf

# Quick page count
pdftotext /path/to/file.pdf | grep -c "Page" | wc -l
```

---

## Artifact Locations

All analysis reports go to:
- `workspace/reports/pdf-analysis/` — PDF analysis reports
- `workspace/config/` — PDF processing configuration

---

## Version History

- 1.0.0 — Initial release

---

*PDF reader skill ready for skill development.*
