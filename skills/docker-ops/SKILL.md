---
name: docker-ops
version: 1.0.0
description: |
  Docker container management, monitoring, and service deployment in the AAC stack.

when_to_use:
  - Managing Docker containers in AAC stack
  - Deploying new services
  - Viewing logs and metrics
  - Restarting services
  - Container cleanup

when_not_to_use:
  - Just listing containers (use 'docker-running' helper)
  - Checking container status (use 'docker-check' helper)
  - Non-Docker service management

tools_involved:
  - docker-cli
  - docker-compose

network_policy: none
expected_artifacts:
  - Container status reports
  - Service logs
  - Deployment configurations

success_criteria:
  - Service deployed and healthy
  - Container status green
  - Logs accessible

---

## Workflows

### deploy_service

Deploys a new service to the AAC Docker stack.

**Parameters:**
- `name`: Service name
- `image`: Docker image
- `port`: Internal port
- `env_file`: Path to .env file

**Steps:**
1. Update `~/stack/docker-compose.yml`
2. Add service configuration
3. `cd ~/stack`
4. `docker compose pull $name`
5. `docker compose up -d $name`
6. Verify health: `docker ps | grep $name`

**Examples:**
```bash
# Deploy new service
deploy_service redis redis:7
# Output: Redis deployed on port 6379
```

---

### restart_service

Restarts a specific Docker container.

**Parameters:**
- `service`: Service name (e.g., n8n, portainer)

**Steps:**
1. `docker restart $service`
2. Wait for health check
3. View logs: `docker-log $service --lines 50`

**Examples:**
```bash
# Restart n8n
restart_service n8n
# Output: n8n restarted, showing last 50 lines
```

---

### check_health

Checks health status of all AAC services.

**Parameters:**
None

**Steps:**
1. Run `docker-check` helper
2. Review status for each service
3. Identify any services showing "stopped"

**Output:**
```
=== AAC Services Status ===
✅ portainer: running
✅ n8n: running
✅ qdrant: running
✅ code-server: running
✅ overseer: running

Total running: 5
```

**Examples:**
```bash
# Check all services
check_health
```

---

### view_logs

Views recent logs from a container.

**Parameters:**
- `service`: Service name
- `lines`: Number of lines (default: 100)
- `follow`: Follow logs in real-time (true/false)

**Steps:**
1. `docker-log $service --lines $lines`
2. If `follow=true`: `docker-follow $service`

**Examples:**
```bash
# View last 100 lines of n8n logs
view_logs n8n 100

# Follow logs in real-time
view_logs n8n 100 true
```

---

### cleanup

Removes unused Docker images and containers.

**Parameters:**
- `type`: 'all', 'images', 'containers'

**Steps:**
1. `docker-cleanup $type`
2. Review cleanup summary
3. Confirm removal

**Examples:**
```bash
# Clean up everything
cleanup all

# Clean up only old images
cleanup images
```

---

## Templates

### service_template

Standard service configuration for docker-compose.yml:

```yaml
  service-name:
    image: image-name:tag
    container_name: container-name
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - KEY=value
    volumes:
      - ./data:/data
```

---

### docker_compose_addition

Adding a new service to the stack:

```yaml
# Add to ~/stack/docker-compose.yml

  new-service:
    image: nginx:latest
    container_name: new-service
    ports:
      - "127.0.0.1:8080:80"
    networks:
      - aac-network
```

---

## Guardrails

1. **Always bind to 127.0.0.1** — Never expose ports publicly
2. **Use container names** — Not auto-generated IDs
3. **Restart properly** — Use `docker restart`, not kill
4. **Check logs first** — Before restarting, check for errors
5. **Keep .env synced** — Update secrets in single place

---

## Negative Examples

### When NOT to use this skill

- Checking container status → Use `docker-check` helper
- Viewing all containers → Use `docker-all` helper
- Just looking at process → Use `docker-stats` helper

### What to do instead

**Instead of:**
```
deploy_service my-service
```

**Do:**
```
# First check if service exists
docker ps | grep my-service

# If exists, just restart it
restart_service my-service
```

---

## Artifact Locations

All artifacts created by this skill go to:
- `~/stack/docker-compose.yml` — Service definitions
- `~/stack/.env` — Environment variables
- Service logs — Available via `docker-log` helper

---

## Service List

Current AAC services:
- portainer (9000) — Container management
- n8n (5678) — Workflow automation
- qdrant (6333) — Vector database
- code-server (8443) — Browser IDE
- overseer (8501) — Monitoring dashboard

---

## Version History

- 1.0.0 — Initial release with Docker operations
