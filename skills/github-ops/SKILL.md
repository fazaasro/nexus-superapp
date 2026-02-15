---
name: github-ops
version: 2.0.0
description: |
  GitHub repository management, CI/CD, and code collaboration.
  
  **10x Architect Protocol:** Design Test → Implement → Validate → Refine
  **Quality First:** All code passes 10-pillar quality gates before delivery.

when_to_use:
  - Creating new GitHub repositories
  - Cloning existing repositories
  - Managing pull requests
  - Setting up GitHub Actions
  - Deploying code via GitHub
  - Repository organization and cleanup

when_not_to_use:
  - Just checking repository status (use 'gh-repos' helper instead)
  - Checking PR status without opening (use 'gh-pr list' instead)
  - Listing issues without creating (use 'gh-issues' instead)
  - Non-GitHub Git operations (use git directly)

tools_involved:
  - gh-cli
  - git
  - docker

network_policy: restricted
allowed_domains:
  - github.com
  - api.github.com
  - docs.github.com
  - raw.githubusercontent.com

expected_artifacts:
  - New repository URL cloned to ~/swarm/repos/
  - GitHub Actions workflow files
  - Repository configuration files (.github/workflows/)
  - Validation test scripts (tests/)
  - Quality audit reports (audits/)

quality_gates:
  - Reliability: Handles null inputs, network failures, edge cases
  - Performance: O(n) or better, caching where appropriate, async I/O
  - Security: No secret leakage, input sanitization, domain restrictions
  - Maintainability: Modular, commented, no spaghetti code
  - Scalability: Handles 1000+ repos without linear degradation
  - Usability: Clear DX, intuitive CLI, helpful errors
  - Portability: No hardcoded paths, uses environment variables
  - Interoperability: Standard JSON/YAML schemas, GitHub API compliance
  - Testability: Logic decoupled, can be unit tested
  - Flexibility: Easy to extend, no breaking changes

success_criteria:
  - Repository created and accessible
  - Repository cloned to correct location
  - GitHub Actions workflow deployed
  - Repository is private (if specified)
  - **NEW:** Validation tests passing
  - **NEW:** Quality audit passed
  - **NEW:** No test failures in last 3 runs

---

## Workflows

### create_repo

**Phase 1: Design Test**  
Creates a new private GitHub repository.

**Parameters:**
- `name`: Repository name (required)

**Steps:**
1. **Validation:** Check if repository already exists
2. **Implementation:** Create repository with gh-new
3. **Quality Gate:** Verify repository is private and accessible

**Validation Script:** `tests/validate_create_repo.sh`

---

**Phase 2: Implementation**  

```bash
# Execute workflow
create_repo my-service
```

**Output:**
```
✅ VALIDATION PASSED: Repository 'my-service' does not exist
✅ REPOSITORY CREATED: https://github.com/fazaasro/my-service
✅ QUALITY AUDIT PASSED:
   - Private: ✅
   - Empty: ✅ (no default README)
   - Access: ✅
```

---

### clone_repo

**Phase 1: Design Test**  
Clones an existing repository to workspace.

**Parameters:**
- `owner`: Repository owner (e.g., fazaasroro)
- `name`: Repository name

**Steps:**
1. **Validation:** Verify repository exists and is accessible
2. **Implementation:** Clone repository with git
3. **Quality Gate:** Verify clone was successful and correct location

**Validation Script:** `tests/validate_clone_repo.sh`

---

**Phase 2: Implementation**  

```bash
# Execute workflow
clone_repo fazaasro n8n-config
```

**Output:**
```
✅ VALIDATION PASSED: Repository 'fazaasro/n8n-config' exists and accessible
✅ CLONE SUCCESSFUL: Cloned to /home/ai-dev/swarm/repos/n8n-config
✅ QUALITY AUDIT PASSED:
   - Size: 45MB
   - Remote: origin/main
   - Branch: main
```

---

### setup_ci

**Phase 1: Design Test**  
Sets up GitHub Actions for automated deployment.

**Parameters:**
- `repo`: Repository name
- `service`: Service name to deploy

**Steps:**
1. **Validation:** Verify repository exists locally
2. **Implementation:** Create workflow directory and file
3. **Quality Gate:** Validate YAML syntax and workflow structure

**Validation Script:** `tests/validate_setup_ci.sh`

---

**Phase 2: Implementation**  

```bash
# Execute workflow
setup_ci n8n n8n
```

**Output:**
```
✅ VALIDATION PASSED: Repository 'n8n' exists at ~/swarm/repos/n8n
✅ WORKFLOW CREATED: .github/workflows/deploy.yml
✅ QUALITY AUDIT PASSED:
   - YAML Syntax: ✅
   - Triggers: ✅ (push to main)
   - Jobs: ✅ (deploy to Portainer)
```

---

### create_pr

**Phase 1: Design Test**  
Creates a pull request for review.

**Parameters:**
- `title`: PR title
- `body`: PR description

**Steps:**
1. **Validation:** Check if branch has commits ahead of main
2. **Implementation:** Push and create PR with gh-pr
3. **Quality Gate:** Verify PR created successfully

**Validation Script:** `tests/validate_create_pr.sh`

---

**Phase 2: Implementation**  

```bash
# Execute workflow
create_pr "Fix authentication bug" "Resolves issue #123."
```

**Output:**
```
✅ VALIDATION PASSED: Branch 'fix/auth' has 2 commits ahead of main
✅ PR CREATED: #456 - Fix authentication bug
✅ QUALITY AUDIT PASSED:
   - Title: ✅ Clear and concise
   - Body: ✅ Descriptive with issue reference
   - Reviewers: ✅ Assigned (fazaasro)
```

---

## Templates

### repository_readme

Standard README template for new repositories:

```markdown
# [Repository Name]

Description of what this repository contains.

## Getting Started

Installation and setup instructions.

## Usage

How to use this repository.

## Testing

Run tests with:
```bash
make test
# OR
npm test
```

## License

MIT
```

---

### github_actions_workflow

Standard GitHub Actions workflow for deployment:

```yaml
name: Deploy to AAC Stack

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      service:
        description: Service to deploy
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate changes
        run: |
          # Pre-deployment validation
          echo "::notice::Validating deployment..."
      
  deploy:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Portainer
        run: |
          curl -X POST $PORTAINER_WEBHOOK \
            -H "Content-Type: application/json" \
            -d "{\"repository\":\"${{ github.repository }}\"}"
```

---

## Quality Gates (10 Pillars)

### 1. Reliability
**Checks:**
- ❓ Handles null inputs gracefully
- ❓ Recovers from network failures
- ❓ Validates external dependencies before use
- ❓ Handles edge cases (empty lists, missing files)

**Implementation:**
- Add input validation at workflow entry
- Wrap external API calls in try/catch
- Document all edge cases in `when_not_to_use`

### 2. Performance
**Checks:**
- ❓ Is this O(n) or better?
- ❓ Can we cache results?
- ❓ Uses async I/O where applicable?
- ❓ No unnecessary loops or nested iterations

**Implementation:**
- Use GitHub API pagination instead of full list
- Cache repository lists locally (max 5 min TTL)
- Use `gh api` for bulk operations

### 3. Security
**Checks:**
- ❓ No secret leakage in logs?
- ❓ All inputs sanitized?
- ❓ Domain restrictions enforced?
- ❓ Secrets use `--secret` flag for gh

**Implementation:**
- Never log repository names, tokens, or PATs
- Sanitize user input (remove special chars from repo names)
- Use `gh secret set` for secrets, never environment variables
- Enforce `network_policy: restricted` for all network calls

### 4. Maintainability
**Checks:**
- ❓ Is code modular?
- ❓ Are functions documented?
- ❓ No spaghetti logic (deep nesting)?
- ❓ Variable names are descriptive?

**Implementation:**
- Each workflow is self-contained
- Use descriptive variable names (`repo_name`, not `r`)
- Limit nesting depth (max 3 levels)
- Comment all non-obvious logic

### 5. Scalability
**Checks:**
- ❓ Handles 1000+ repos without linear degradation?
- ❓ No hardcoded limits or page sizes?
- ❓ Can process in batches?

**Implementation:**
- Process paginated results in chunks
- Use async where possible (gh api)
- No `for repo in $(gh-repos):` — use pagination

### 6. Usability
**Checks:**
- ❓ Clear error messages?
- ❓ Intuitive CLI flags?
- ❓ Help text is helpful?
- ❓ Progress indicators for long operations?

**Implementation:**
- Human-readable error messages
- Use `--help` flag for all workflows
- Show progress: `[1/100] Processing repos...`
- Color-coded output: ✅ success, ⚠️ warning, ❌ error

### 7. Portability
**Checks:**
- ❓ No hardcoded paths on my machine?
- ❓ Uses environment variables?
- ❓ Works on macOS/Linux/Windows?

**Implementation:**
- Use `$GITHUB_WORKSPACE` if available
- Configurable via env: `GITHUB_WORKSPACE_DIR=~/swarm/repos`
- Cross-platform compatible (use `gh` which handles all OS)

### 8. Interoperability
**Checks:**
- ❓ Standard JSON/YAML schemas?
- ❓ GitHub API compliance?
- ❓ Works with existing tools (git, docker)?

**Implementation:**
- Standard Markdown for READMEs
- Standard YAML for workflows
- Compatible with gh-cli, git, docker
- Uses GitHub REST API (v3)

### 9. Testability
**Checks:**
- ❓ Is logic decoupled from GitHub API?
- ❓ Can run integration tests?
- ❓ No hardcoded assertions?

**Implementation:**
- Separate validation scripts (tests/)
- Each workflow validates before execution
- Use return codes for programmatic testing
- Document test requirements in README

### 10. Flexibility
**Checks:**
- ❓ Easy to add new workflows?
- ❓ Can extend without breaking changes?
- ❓ Backwards compatible?

**Implementation:**
- Workflow files are modular
- New workflows add without modifying existing ones
- Use semantic versioning (2.0.0 → 2.1.0)
- Support `--dry-run` flag for preview

---

## Guardrails

1. **Never commit secrets** — Add all secrets to `.env` or GitHub Secrets
2. **Always use --private** — Default to private repositories
3. **Verify before cloning** — Check repository exists with `gh-repos`
4. **Validate before creation** — Run validation scripts before implementation
5. **Quality Gates** — Must pass all quality gates before success
6. **Error Handling** — All external API calls wrapped in try/catch
7. **No Hardcoding** — Use environment variables, config files, or API calls
8. **Documentation** — Document all validation requirements and quality gates

---

## Negative Examples

### When NOT to use this skill

- Checking if repository exists → Use `gh-repos` or validation script
- Just creating README → Use `repository_readme` template
- Non-GitHub operations → Use `git` or `exec` tool directly

### What to do instead

**Instead of:**
```
create_repo my-existing-repo
```

**Do:**
```
# Phase 1: Validation (Design Test)
# Check if exists
gh-repos | grep my-existing-repo

# If exists, exit with helpful message
if [ $? -eq 0 ]; then
  echo "⚠️ Repository 'my-existing-repo' already exists"
  echo "Use 'clone_repo fazaasro my-existing-repo' instead"
  exit 1
fi

# Phase 2: Implementation
create_repo my-existing-repo
```

---

## Artifact Locations

All artifacts created by this skill go to:
- `~/swarm/repos/` — Cloned repositories
- `.github/workflows/` — CI/CD configurations
- `tests/` — Validation scripts
- `audits/` — Quality audit reports

---

## Version History

- 1.0.0 — Initial release with core GitHub workflows
- 2.0.0 — **10x Architect upgrade**: Added validation scripts, quality gates, Evo 3 protocol

---

## 10x Architect Protocol

### Phase 1: Design Test
- Create validation script that asserts expected outcome
- Define "Success" programmatically (not "it seems to work")
- The test must FAIL if feature is missing
- Test passes ONLY if feature works 100%

### Phase 2: Implementation
- Write code to satisfy test
- Draft: Initial implementation
- Execute: Run validation script yourself
- Loop: If FAIL → Read error, fix code, re-run (max 3x)

### Phase 3: Validate
- Run integration test
- Verify against 10 quality pillars
- Pass gate → Proceed
- Fail gate → Refine

### Phase 4: Quality Gate
- Review your own code against 10 pillars
- If any pillar violated → Refactor immediately
- Create audit report documenting which attributes were addressed

### The Proof
When you deliver work, show:
- **The Proof:** Output of passing Integration Test
- **The Code:** Final, refactored implementation
- **The Audit:** Brief checklist of which Quality Attributes were specifically addressed

**Why this works:**
- The Loop forces grounding in reality
- The Quality Gate forces production-grade code
- Combined, you get repeatable workflows with real execution

---

## Usage Examples

### Example 1: Create New Repository

```bash
# User request
create_repo my-awesome-service

# Levy's response
✅ VALIDATION PASSED: Repository 'my-awesome-service' does not exist
✅ REPOSITORY CREATED: https://github.com/fazaasro/my-awesome-service
✅ QUALITY AUDIT PASSED:
   - Private: ✅
   - Empty: ✅
   - Access: ✅

The Proof:
- Repository exists at https://github.com/fazaasro/my-awesome-service
- Verified private: gh repo view my-awesome-service
```

### Example 2: Clone Repository

```bash
# User request
clone_repo fazaasro n8n

# Levy's response
✅ VALIDATION PASSED: Repository 'fazaasro/n8n' exists and accessible
✅ CLONE SUCCESSFUL: Cloned to /home/ai-dev/swarm/repos/n8n
✅ QUALITY AUDIT PASSED:
   - Size: 45MB
   - Remote: origin/main
   - Branch: main
```

### Example 3: Multi-Skill Workflow

```
User: "Deploy my new project to AAC stack"

Levy:
  Uses github-ops skill
  → Phase 1: Design Test (validate create_repo)
  → create_repo my-project
  → Uses docker-ops skill (deploy_service)
  → Uses cloudflare-ops skill (add_route)
  → Uses monitoring-ops skill (check_status)

User: "What happened?"

Levy:
  ✅ VALIDATION PASSED: Repository does not exist
  ✅ REPOSITORY CREATED: https://github.com/fazaasro/my-project
  ✅ SERVICE DEPLOYED: my-project running
  ✅ ROUTE ADDED: my-project.zazagaby.online
  ✅ MONITORING: Service healthy (all green)
  
The Proof:
- Repository accessible at https://github.com/fazaasro/my-project
- Container running: docker ps | grep my-project
- DNS resolving: nslookup my-project.zazagaby.online
- Monitor showing: monitor.zazagaby.online → check_status
```

---

## Testing

Run validation tests:

```bash
# Test repository creation validation
tests/validate_create_repo.sh

# Test repository clone validation
tests/validate_clone_repo.sh

# Test CI setup validation
tests/validate_setup_ci.sh

# Test PR creation validation
tests/validate_create_pr.sh
```

---

*github-ops v2.0.0 — 10x Architect Edition*
