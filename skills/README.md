# Levy Skills Registry

**Version:** 1.0.0  
**Last Updated:** 2026-02-12

---

## Available Skills

| Skill | Version | Description | SKILL.md Location |
|--------|---------|-------------|------------------|
| **github-ops** | 2.0.0 | GitHub repository management, CI/CD, 10x Architect protocol | `skills/github-ops/SKILL.md` |
| **docker-ops** | 1.0.0 | Docker container management | `skills/docker-ops/SKILL.md` |
| **cloudflare-ops** | 1.0.0 | Cloudflare tunnel & DNS management | `skills/cloudflare-ops/SKILL.md` |
| **monitoring-ops** | 1.0.0 | Overseer dashboard operations | `skills/monitoring-ops/SKILL.md` |

---

## Quick Reference

### GitHub Operations

**Use when:** Creating/managing repositories, setting up CI/CD
```bash
# Create repository
Use: github-ops skill → create_repo my-project

# Clone repository
Use: github-ops skill → clone_repo fazaasro my-repo

# Set up GitHub Actions
Use: github-ops skill → setup_ci my-service
```

### Docker Operations

**Use when:** Deploying/managing Docker services
```bash
# Deploy new service
Use: docker-ops skill → deploy_service redis redis:7

# Restart service
Use: docker-ops skill → restart_service n8n

# Check health
Use: docker-ops skill → check_health

# View logs
Use: docker-ops skill → view_logs n8n 100
```

### Cloudflare Operations

**Use when:** Managing tunnels, DNS, Access policies
```bash
# Create tunnel
Use: cloudflare-ops skill → create_tunnel my-tunnel

# Add DNS route
Use: cloudflare-ops skill → add_route abc123 myapp

# Test URL
Use: cloudflare-ops skill → test_url https://myapp.zazagaby.online

# Configure Access
Use: cloudflare-ops skill → configure_access "My App" myapp fazaasro@gmail.com
```

### Monitoring Operations

**Use when:** Checking system health, reviewing metrics
```bash
# Check status
Use: monitoring-ops skill → check_status

# Review trends
Use: monitoring-ops skill → review_trends 24h

# Check security
Use: monitoring-ops skill → check_security

# Analyze OpenClaw
Use: monitoring-ops skill → analyze_openclaw
```

---

## Skill Invocation Patterns

### Single-Skill Workflows

**Example: Deploy new service**
```
User: "Deploy a new Redis service"

Levy: 
  Uses docker-ops skill
  → Creates service definition in docker-compose.yml
  → Deploys container
  → Verifies health

User: "Now add a DNS route for it"

Levy:
  Uses cloudflare-ops skill
  → Adds route to tunnel
  → Tests access
  
User: "Set up monitoring"

Levy:
  Uses monitoring-ops skill
  → Configures alert thresholds
  → Reviews dashboard
```

### Multi-Skill Workflows

**Example: Create and deploy new project**
```
User: "Create a new project called 'todo-app' with GitHub Actions"

Levy:
  Uses github-ops skill
  → create_repo todo-app
  → setup_ci todo-app
  → clone_repo todo-app

Levy:
  Uses docker-ops skill
  → deploy_service todo-app

Levy:
  Uses cloudflare-ops skill
  → add_route todo-app

Levy:
  Uses monitoring-ops skill
  → check_status
```

---

## Helper Scripts Reference

All helper scripts are in `~/scripts/`:

| Script | Purpose |
|--------|---------|
| `gh-helpers.sh` | GitHub CLI commands (gh-repos, gh-new, gh-pr, etc.) |
| `cf-helpers.sh` | Cloudflare commands (cf-tunnels, cf-route, cf-test, etc.) |
| `docker-helpers.sh` | Docker commands (docker-check, docker-log, docker-restart, etc.) |
| `helpers.sh` | Main loader (run `levy-help` to see all commands) |

---

## Artifact Locations

| Type | Location |
|-------|----------|
| **Skills** | `skills/*/SKILL.md` |
| **Helper Scripts** | `scripts/*.sh` |
| **Documentation** | `workspace/*.md` |
| **Artifacts** | `workspace/reports/`, `workspace/config/` |

---

## Best Practices

1. **Always check `when_to_use`** — Skills describe when to use/not use
2. **Read success criteria** — Know what "done" looks like
3. **Follow workflows** — Multi-step procedures are documented
4. **Use guardrails** — Security and safety guidelines
5. **Check artifacts** — Verify outputs are written correctly

---

## Future Skills (Planned)

### Phase 2
- **calendar-ops** — Google Calendar management via gog
- **email-ops** — Gmail management and automation
- **project-ops** — Project file organization and search

### Phase 3
- **deployment-ops** — Automated deployment pipelines
- **backup-ops** — Backup and restore procedures
- **testing-ops** — Automated testing workflows

---

## Skill Metadata

Each skill includes:
- `name`: Skill identifier
- `version`: Semantic version
- `description`: What the skill does
- `when_to_use`: When to invoke
- `when_not_to_use`: When NOT to invoke
- `tools_involved`: Tools used by the skill
- `workflows`: Available procedures
- `templates`: Reusable templates
- `guardrails`: Safety guidelines
- `negative_examples`: Anti-patterns

---

*Skills Registry — Managed by Levy 🏗️*
