# Levy Improvement Plan — Agentic Primitives

**Based on:** OpenAI Developers Blog — "Shell + Skills + Compaction: Tips for long-running agents"  
**Source:** https://openai.com/blog/shell-skills-compaction  
**Date:** 2026-02-12

---

## Core Concepts

### 1. Skills = Procedures
A **skill** is a bundle of files plus a `SKILL.md` manifest containing:
- Frontmatter (name, description, version)
- Instructions (workflows, procedures)
- Examples (when to use, when not to use)

**Why?** Reduces prompt spaghetti by moving stable procedures into reusable bundles.

### 2. Shell = Execution
A **shell tool** provides a real terminal environment where agents can:
- Install dependencies
- Run scripts
- Write outputs (reports, artifacts)

**OpenClaw equivalent:** `exec` tool (already available)

### 3. Compaction = Continuity
**Server-side compaction** automatically:
- Manages context window
- Compresses conversation history
- Preserves continuity across long runs

**Levy status:** ✅ Compaction enabled (mode: safeguard)

---

## Levy's Current State

| Component | Status | Notes |
|-----------|--------|-------|
| **Skills** | ⚠️ Informal | Documented in separate files, no SKILL.md format |
| **Shell** | ✅ Available | `exec` tool on VPS |
| **Compaction** | ✅ Enabled | Safeguard mode |
| **Artifact Boundary** | ✅ Defined | `/home/ai-dev/.openclaw/workspace/` |
| **Network Access** | ✅ Controlled | `exec` tool, `web_search`, `web_fetch` |
| **Allowlists** | ⚠️ Basic | No org-level allowlist configured |

---

## Improvement Areas

### 1. Create Skills with SKILL.md Format

**Current:** Procedures scattered across multiple files
- `TOOLS.md` — Infrastructure reference
- `SETUP_GUIDE.md` — Quick start
- `INTEGRATION_GUIDE.md` — Integration docs

**Better:** Encode procedures as formal skills

**Example Skill Structure:**
```
---
name: github-ops
version: 1.0.0
description: GitHub repository management and CI/CD operations

when_to_use:
  - Creating GitHub repositories
  - Managing pull requests
  - Setting up GitHub Actions
  - Deploying via GitHub

when_not_to_use:
  - Just reading repository info (use gh-repos instead)
  - Local file operations (use exec instead)

workflow:
  1. gh-new $name --private
  2. git clone $name
  3. cd $name
  4. git remote set origin git@github.com:...
  5. git push -u origin main

examples:
  - input: "Create a new private repo called my-project"
    output: gh-new my-project --private
    
  - input: "Deploy n8n workflow"
    output: cd ~/swarm/repos/n8n && git push origin main
```

---

### 2. Add Routing Logic to Skill Descriptions

**Principle:** Write skill descriptions like routing logic (not marketing copy)

**Current:** Generic descriptions like "GitHub helper"

**Better:** Explicit decision boundaries:
- When should I use this?
- When should I NOT use this?
- What are the outputs and success criteria?
- What tools are involved?

**Example:**
```
description: |
  Creates and manages GitHub repositories.
  
  USE WHEN: You need persistent Git repositories with GitHub Actions integration.
  DON'T USE WHEN: Only checking repo status (use 'gh-repos' instead).
  
  TOOLS INVOLVED: gh-cli, git, docker
  EXPECTED ARTIFACT: New repository URL cloned to ~/swarm/repos/
  
  SUCCESS: Repository created, cloned, and GitHub Actions workflow ready.
```

---

### 3. Add Negative Examples and Edge Cases

**Principle:** Reduce misfires with explicit "don't use when" cases

**Example:**
```
when_not_to_use:
  - Repository already exists (use gh-repos to check first)
  - Just listing repositories (use gh-repos, not gh-new)
  - Checking PR status without opening (use gh-pr list)
  - Non-GitHub Git operations (use git directly)
```

---

### 4. Move Templates to Skills

**Current:** Templates often in system prompts or READMEs

**Better:** Put templates in SKILL.md (free when unused)

**Example — Deployment Template:**
```
templates:
  docker_deploy: |
    #!/bin/bash
    # Deploy service to Docker stack
    SERVICE=$1
    docker-compose pull $SERVICE
    docker-compose up -d $SERVICE
    docker ps | grep $SERVICE
```

---

### 5. Design for Long Runs

**Principles:**
- Reuse containers across steps
- Use `/home/ai-dev/.openclaw/workspace/` as artifact boundary
- Keep intermediate outputs in workspace
- Use consistent file naming

**Example — Multi-Step Workflow:**
```
Step 1: Analyze logs → workspace/logs-analysis.md
Step 2: Generate report → workspace/reports/weekly.md
Step 3: Create summary → workspace/summaries/digest.md

All artifacts in known location, easy to reference.
```

---

### 6. Explicit Skill Invocation

**Principle:** When you need determinism, explicitly tell the model

**Current:** Model decides when to use procedures

**Better:** Add direct command for critical workflows

**Examples:**
- "Use the github-ops skill to deploy the n8n update"
- "Use the cloudflare-ops skill to add the new route"
- "Use the monitoring skill to check service status"

---

### 7. Treat Networking as High-Risk

**Principle:** Skills + networking = design for containment

**Current:** Many tools can access internet (web_search, web_fetch, browser)

**Better:** Add safety boundaries:

**In Skill Description:**
```
network_policy: restricted
allowed_domains:
  - github.com
  - docs.openclaw.ai
  - clawhub.com
output_trust: untrusted  # Treat as untrusted content
```

**In Usage:**
- Never execute code from untrusted sources
- Sanitize all web content (SECURITY NOTICE)
- Ask before making network calls

---

### 8. Define Artifact Boundary

**Principle:** `/mnt/data` (or equivalent) is the handoff boundary

**Levy's Boundary:** `/home/ai-dev/.openclaw/workspace/`

**Usage:**
- All reports written to `workspace/reports/`
- All configs in `workspace/config/`
- All artifacts in `workspace/artifacts/`

**Cleanup:** Periodically remove old artifacts to prevent bloat

---

### 9. Understand Allowlists as Two-Layer System

**Levy Status:** No org-level allowlist configured

**Implementation:**
- **Org-level:** (None) Could add to `openclaw.json` — `shell.network.allowedDomains`
- **Request-level:** Each exec call can specify what's allowed

**Example:**
```
network_policy:
  org_allowlist:
    - github.com
    - docs.openclaw.ai
    - zazagaby.online
  request_allowlist:
    - api.openai.com
    - api.anthropic.com
    - api.zai.com
```

---

### 10. Use Domain Secrets for Auth

**Principle:** Never expose raw credentials

**Current:** Some secrets in `.env` (marked "NEVER COMMIT")

**Better:** Use OpenClaw's secrets management

**Example:**
```
# Instead of:
CF_API_TOKEN=67685adc08f6a53ed01c79a718f67060e38a7

# Use:
$CF_API_TOKEN  # Placeholder, injected by OpenClaw
```

---

## Action Plan

### Phase 1: Create Formal Skills (Immediate)
1. Convert existing procedures to SKILL.md format:
   - `github-ops` — GitHub management
   - `docker-ops` — Docker operations
   - `cloudflare-ops` — Cloudflare tunnel management
   - `monitoring-ops` — Overseer dashboard operations

2. Add routing logic, negative examples, templates
3. Create `skills/` directory in workspace

### Phase 2: Improve Documentation (Week 1)
1. Create standard artifact structure
2. Add networking safety guidelines to all skills
3. Document skill invocation patterns

### Phase 3: Build Repeatable Workflows (Week 2-3)
1. Encode common workflows as skills
2. Add intermediate output management
3. Implement cleanup procedures

### Phase 4: Advanced (Month 2)
1. Create skills that call other skills
2. Implement request-level allowlists
3. Add domain secrets usage

---

## Example: github-ops Skill

```markdown
---
name: github-ops
version: 1.0.0
description: |
  GitHub repository management, CI/CD, and code collaboration.
  
  USE WHEN: Creating/managing GitHub repositories, setting up Actions, or handling PRs.
  DON'T USE WHEN: Just checking repo status (use 'gh-repos' helper instead).
  
  TOOLS INVOLVED: gh-cli, git, docker
  NETWORKING: Required (github.com, api.github.com)
  
  SUCCESS CRITERIA: Repository created/cloned and accessible in ~/swarm/repos/

when_to_use:
  - Creating new repositories
  - Cloning repositories
  - Setting up GitHub Actions
  - Managing pull requests
  - Deploying code

when_not_to_use:
  - Just listing repositories (use `gh-repos`)
  - Checking PR status (use `gh-pr list`)
  - Non-GitHub Git operations (use `git` directly)

workflow:
  create_repo:
    description: Create a new private repository
    steps:
      1. gh-new $name --private
      2. git clone $name
      3. cd $name && echo "# $name" > README.md
      4. git add . && git commit -m "Initial commit"
      5. git push -u origin main
  
  setup_ci:
    description: Set up GitHub Actions workflow
    steps:
      1. cd ~/swarm/repos/$repo
      2. mkdir -p .github/workflows
      3. Create workflow.yml template
      4. git push origin main

examples:
  - input: "Create a new private repo called my-service"
    output: |
      gh-new my-service --private
      # Repository created: https://github.com/fazaasro/my-service
  
  - input: "Deploy n8n with GitHub Actions"
    output: |
      cd ~/swarm/repos/n8n
      # Create .github/workflows/deploy.yml
      git push origin main
      # GitHub Actions will deploy
```

---

## Metrics to Track

| Metric | Current | Target |
|---------|---------|--------|
| Skill count | ~5 docs | 20 formal skills |
| Skill usage rate | N/A | Track in sessions |
| Artifact bloat | N/A | Periodic cleanup |
| Routing accuracy | N/A | <5% misfires |
| Long-run success | N/A | >90% completion |

---

## References

- OpenAI Blog: https://openai.com/blog/shell-skills-compaction
- Skills Guide: https://docs.openclaw.ai/skills
- ClawHub: https://clawhub.com

---

*Improvement plan created by Levy 🏗️*
