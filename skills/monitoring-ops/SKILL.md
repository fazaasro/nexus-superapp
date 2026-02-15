---
name: monitoring-ops
version: 1.0.0
description: |
  Overseer monitoring dashboard operations, metrics collection, and alerting for the AAC infrastructure.

when_to_use:
  - Checking system health via Overseer
  - Analyzing metrics and trends
  - Viewing security events
  - Checking service statuses
  - Reviewing token usage and tool statistics

when_not_to_use:
  - Just viewing current metrics (use Overseer dashboard instead)
  - Non-monitoring system checks
  - One-time health checks (use individual service checks)

tools_involved:
  - overseer-dashboard (web interface)
  - sqlite-query (for direct data access)

network_policy: restricted
allowed_domains:
  - monitor.zazagaby.online
  - zazagaby.online

expected_artifacts:
  - Health reports
  - Security event logs
  - Performance analysis

success_criteria:
  - Dashboard accessible
  - Metrics collecting properly
  - Security events captured
  - Alerts triggered correctly

---

## Workflows

### check_status

Checks overall status of all monitored services via Overseer.

**Parameters:**
None

**Steps:**
1. Navigate to https://monitor.zazagaby.online
2. Review "Health Status" tab
3. Check service status indicators
4. Review metrics trends

**Output:**
```
Service Status:
  n8n: ✅ Healthy (200ms latency)
  portainer: ✅ Healthy (150ms latency)
  qdrant: ✅ Healthy (80ms latency)
  code-server: ✅ Healthy (200ms latency)

Security: ✅ No SSH failures (last hour)
Fail2Ban: 0 banned IPs
```

**Examples:**
```bash
# Check status via dashboard
check_status
# Output: Shows status from monitor.zazagaby.online
```

---

### review_trends

Analyzes performance trends over time.

**Parameters:**
- `period`: Time period (default: 24h)

**Steps:**
1. Navigate to Overseer dashboard
2. Select "Trends" tab
3. Review CPU, RAM, and latency charts
4. Identify any spikes or degradation

**Metrics to Review:**
- CPU usage trends
- RAM usage patterns
- Application latency over time
- Network I/O patterns

**Examples:**
```bash
# Review last 24 hours
review_trends 24h
# Output: Shows trends from dashboard
```

---

### check_security

Reviews security events and threats.

**Parameters:**
None

**Steps:**
1. Navigate to "Security" tab
2. Review SSH failure count
3. Check Fail2Ban banned IPs
4. Review security event log

**Alerts to Monitor:**
- SSH brute force attempts (>10/hour)
- Banned IP count spikes
- Unusual login patterns

**Examples:**
```bash
# Check security status
check_security
# Output: Shows security events
```

---

### view_network

Reviews network status and port status.

**Parameters:**
None

**Steps:**
1. Navigate to "Network" tab
2. Review open ports
3. Check network traffic (in/out)
4. Verify only expected ports are open

**Expected Open Ports:**
- 22 (SSH via Cloudflare)
- 9000 (Portainer)
- 5678 (n8n)
- 6333 (Qdrant)
- 8443 (Code-Server)
- 8501 (Overseer)
- 18789 (OpenClaw)

**Examples:**
```bash
# Check network status
view_network
# Output: Shows ports and traffic
```

---

### analyze_openclaw

Reviews OpenClaw agent metrics.

**Parameters:**
None

**Steps:**
1. Navigate to "OpenClaw" tab
2. Review active sessions
3. Check average latency
4. Review tool usage frequency
5. Check memory usage

**Metrics to Monitor:**
- Active session count
- Average thought latency
- Tool usage patterns
- Memory consumption

**Examples:**
```bash
# Analyze OpenClaw performance
analyze_openclaw
# Output: Shows agent metrics
```

---

## Templates

### health_report

Standard health report format:

```markdown
# System Health Report
Date: 2026-02-12 10:00 CET

## Service Status
| Service | Status | Latency |
|---------|--------|---------|
| n8n | ✅ Healthy | 200ms |
| portainer | ✅ Healthy | 150ms |
| qdrant | ✅ Healthy | 80ms |
| code-server | ✅ Healthy | 200ms |

## Security
- SSH Failures: 0 (last hour)
- Fail2Ban Banned IPs: 0
- Security Events: 0

## Recommendations
- No issues detected
- All services operational
```

---

### alert_template

Alert notification template:

```markdown
🚨 ALERT: [Service Name]

**Status:** [Status]
**Time:** [Timestamp]
**Details:** [Details]

**Action Required:** [Action to take]

--- 
Reported by Overseer
```

---

## Guardrails

1. **Check dashboard first** — Don't rely on manual logs if dashboard is available
2. **Verify trends** — Look for patterns, not single data points
3. **Review security regularly** — Daily security check recommended
4. **Set alert thresholds** — Know what triggers notifications
5. **Compare against baselines** — Understand what "normal" looks like

---

## Negative Examples

### When NOT to use this skill

- Checking if service is up → Use `docker-check` helper for container status
- One-time health check → Use `curl` or individual service access
- Accessing raw database → Use dashboard interface

### What to do instead

**Instead of:**
```
check_status
```

**Do:**
```
# For quick container health
docker-check

# For detailed monitoring
navigate to https://monitor.zazagaby.online
```

---

## Artifact Locations

All artifacts created by this skill go to:
- `https://monitor.zazagaby.online` — Dashboard interface
- `/home/ai-dev/swarm/repos/overseer/data/metrics.db` — Metrics database

---

## Dashboard Tabs

1. **Health Status** — Real-time service health
2. **Trends** — Performance charts over time
3. **Security** — Security events and alerts
4. **Network** — Port status and traffic
5. **OpenClaw** — Agent metrics and usage

---

## Version History

- 1.0.0 — Initial release with monitoring operations
