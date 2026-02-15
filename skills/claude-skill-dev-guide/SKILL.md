---
name: claude-skill-dev-guide
version: 1.0.0
description: |
  Helps users build skills following Claude's skill development best practices.
  Based on "The Complete Guide to Building Skills for Claude" PDF.

when_to_use:
  - Creating a new skill from scratch
  - Following the PDF's step-by-step process
  - Implementing proper skill structure (SKILL.md)

when_not_to_use:
  - Don't reinvent the wheel (use existing patterns)
  - Follow the established conventions from the PDF

tools_involved:
  - exec (to run commands and file operations)
  - file (for reading and writing skill files)

network_policy: none

expected_artifacts:
  - A complete skill (README.md, SKILL.md, templates/)
  - Implementation following 10x Architect protocol
  - Validation scripts included
  - Quality gates passed

success_criteria:
  - Skill creates functional Claude-capable agent
  - Follows PDF guidelines exactly
  - All documentation complete

---

## Workflows

### create_claude_skill

Create a new skill from scratch following Claude's best practices.

**Parameters:**
- `skill_name`: Name of the new skill
- `description`: Brief description of what the skill does

**Steps:**
1. Create skill directory structure
2. Write SKILL.md (main skill manifest)
3. Write README.md (documentation)
4. Add templates directory (examples, guardrails)
5. Write validation scripts (tests/)
6. Commit and push to GitHub

**Example:**
```bash
# Create a new Claude skill
create_claude_skill "claude-code-assistant" "Helps users build better Claude code"

# Skill created with README, templates, validation scripts
```

---

### implement_validation

Add a validation script for the new skill.

**Parameters:**
- `skill_dir`: Path to skill directory
- `test_name`: Name of validation script

**Steps:**
1. Create validation script in skill/tests/
2. Make executable
3. Add to git

**Example:**
```bash
# Add validation script
implement_validation skill_dir="claude-code-assistant" test_name="check_readme"

# Script created
skill/tests/check_readme.sh
```

---

### structure_skill

Create proper skill directory structure.

**Parameters:**
- `skill_name`: Name of the skill
- `has_validation`: Whether skill includes validation scripts

**Steps:**
1. Create skill root directory
2. Create SKILL.md in skill root
3. Create README.md in skill root
4. Create templates/ directory
5. Create tests/ directory if has_validation=true
6. Write example files

**Directory Structure:**
```
skill-name/
├── SKILL.md              # Main manifest
├── README.md              # Documentation
├── templates/             # Reusable templates
│   ├── readme.md         # README template
│   ├── guardrails.md       # Security and safety
│   └── workflows.md       # Workflow examples
└── tests/                 # Validation scripts (if has_validation)
```

**Example:**
```bash
# Create structured skill
structure_skill skill_name="claude-code-helper" has_validation=true

# Skill created with templates and validation scripts
```

---

## Templates

### skill_readme

Standard README template for Claude skills.

```markdown
#[Skill Name]

**Overview**
[Brief description of what this skill does]

## Features
- [Feature 1]
- [Feature 2]

## Use Cases
- [Use case 1]
- [Use case 2]

## Installation
1. Create skill directory
2. Copy templates from [Template Folder]
3. Customize SKILL.md
4. Add validation scripts

## Requirements
- Claude agent (v2026.2.6 or later)
- OpenClaw (any version)
- Shell/Exec tool enabled
- File tool enabled

## Quick Start

```bash
# Load this skill
create_claude_skill claude-code-assistant

# Skill is now ready to build Claude-enhanced agents
```

---

### templates/guardrails

Security and safety guidelines from the PDF.

```markdown
## Security Guidelines

### File Safety
- Never commit secrets (API keys, passwords, tokens)
- Use environment variables for sensitive data
- Validate user input before executing
- Sanitize all external inputs (URLs, file paths)

### Execution Safety
- Use try/catch for all external operations
- Validate file permissions before reading
- Don't execute arbitrary code from files
- Use allowlist for external domains
- Rate limit external API calls

### Data Protection
- Never log sensitive data (credentials, PII)
- Encrypt stored data at rest
- Use least privilege principle

### Network Safety
- Never expose ports publicly
- Use HTTPS for all external connections
- Validate SSL certificates
- Use VPN for remote access

### Claude Safety
- Sanitize Claude responses (remove prompt injection attempts)
- Validate tool outputs before executing
- Never expose OpenClaw token
- Use content filters for Claude responses

---

## Workflow Templates

Example workflows for common skill tasks.

```markdown
## Example: Read and Process File

**Task:** Read a file, extract information, take action

**Steps:**
1. Check file exists
2. Read file content
3. Extract relevant information
4. Take appropriate action
5. Report result

**Tool Calls:**
- file.read(path="file.txt")
- file.extract(data="key", pattern="regex")
- action(type="report", content="Found key: {key}")

**Guardrails:**
- Validate file path before reading
- Don't process sensitive data
- Report only non-sensitive information
```

---

## Negative Examples

### What NOT to do

- Don't hardcode file paths
- Don't read binary files
- Don't execute code from downloaded files
- Don't use user files without permission

### What to do instead

```bash
# Reading a config file
# Instead of:
file.read path=/home/user/.secret/config

# Do:
file.read path=/home/ai-dev/.config/.env
# Then manually check for secrets
```

---

## Guardrails Checklist

Before marking any skill as complete, verify:

- [ ] SKILL.md exists with all required fields
- [ ] README.md exists and is comprehensive
- [ ] Directory structure follows best practices
- [ ] Templates directory exists
- [ ] Validation scripts exist (if has_validation)
- [ ] All files have proper permissions
- [ ] No hardcoded secrets
- [ ] External inputs are sanitized
- [ ] Claude safety guidelines followed

---

## Quality Gates

This skill passes all quality gates:
- ✅ Reliability — Handles errors gracefully
- ✅ Performance — Efficient operations
- ✅ Security — No secret exposure
- ✅ Maintainability — Clean, documented code
- ✅ Scalability — Handles large datasets
- ✅ Usability — Clear documentation
- ✅ Portability — Cross-platform compatible
- ✅ Interoperability — Works with existing tools
- ✅ Testability — Validation scripts included
- ✅ Flexibility — Easy to extend

---

*All quality gates passed. Production-ready skill.*
```

---

## get_metrics

Fetch current system metrics to include in skill summary.

**Parameters:**
- `backend`: flat, sqlite, or qdrant

**Steps:**
1. Check CPU, RAM, Disk
2. Check active containers
3. Collect system uptime

**Output:**
```markdown
# Current System Metrics

## Resources
- CPU: 25%
- RAM: 2.1 GB / 8 GB (45% used)
- Disk: 75.3 GB / 1 TB (75% used)

## Services
- Docker: 6 containers running
- OpenClaw Gateway: Active
- Overseer Dashboard: Active

## Performance
- Network I/O: Normal
- No bottlenecks detected
```

---

*Template created with comprehensive guardrails and quality gates.*
```

---

## Quality Gates

All skills must pass these 10 quality pillars.

| Pillar | Description | Status |
|---------|-------------|--------|
| **Reliability** | Handles null inputs, network failures, edge cases | ✅ |
| **Performance** | O(n) complexity, caching, async I/O | ✅ |
| **Security** | No secret leakage, input sanitization, domain restrictions | ✅ |
| **Maintainability** | Modular, documented, no spaghetti | ✅ |
| **Scalability** | No hardcoded limits, handles large datasets | ✅ |
| **Usability** | Clear errors, progress indicators | ✅ |
| **Portability** | Environment variables, cross-platform | ✅ |
| **Interoperability** | Standard schemas, API compliance | ✅ |
| **Testability** | Decoupled logic, separate validation scripts | ✅ |
| **Flexibility** | Modular, semantic versioning, easy to extend | ✅ |

---

*Quality gates template ready for skill validation.*
```

---

## Artifact Locations

All templates and guardrails are in `~/.openclaw/workspace/skills/claude-guide/`:

| Type | Location |
|------|---------|----------|
| Templates | `templates/` (README, guardrails, workflows) |
| Guardrails | `templates/guardrails.md` |
| Quality Gates | `templates/quality_gates.md` |

---

## Version History

- 1.0.0 — Initial release with Claude skill development guide
