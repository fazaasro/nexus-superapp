# Agent 1: Monitoring System Migration Context

## Mission
Reorganize the monitoring system and migrate from Overseer (Streamlit-based) to the Grafana ecosystem. Ensure all current features are preserved and the system scales to monitor everything we do later.

## Current System: Project Panopticon / Overseer

### Location
- **Repo:** `/home/ai-dev/swarm/repos/overseer/`
- **Public URL:** `https://monitor.zazagaby.online/`
- **Stack:** Streamlit + SQLite + Docker

### Current Features (from app.py)

#### 1. **Health Dashboard (Tab 1)**
- Real-time service health checks
- App status cards with health indicators:
  - ✅ Healthy (200 status + <500ms latency)
  - ⚠️ Slow (200 status + >500ms latency)
  - ❌ Down (non-200 status)
- Container status table (running containers only):
  - Container name
  - Status (running/stopped)
  - Restart count
  - Image tag

#### 2. **Trends Dashboard (Tab 2)**
- **CPU Usage** - 24h historical line chart
- **RAM Usage** - 24h historical line chart
- **Application Latency** - Multi-line chart by app name (24h)
- **Token Burn Rate** (24h):
  - Total cost in USD
  - Total token count
  - Bar chart by provider (GLM-4.7, Kimi K2.5, etc.)
- **Tool Usage Frequency** - Bar chart of tool calls (24h)
  - Red highlighting for delete operations

#### 3. **Security Dashboard (Tab 3)**
- SSH failed attempts in last hour
- Fail2Ban banned IPs count
- Security events log (last 50):
  - Timestamp
  - Event type
  - Source IP
  - Details

#### 4. **Network Dashboard (Tab 4)**
- **Open Ports** visualization:
  - 22: SSH
  - 80: HTTP
  - 443: HTTPS
  - 9000: Portainer
  - 5678: n8n
  - 6333: Qdrant
  - 8443: Code-Server
  - 8501: Overseer
  - 18789: OpenClaw
- Network traffic metrics:
  - Network In (MB)
  - Network Out (MB)

#### 5. **OpenClaw Metrics Dashboard (Tab 5)**
- Memory usage (MB)
- Active sessions count
- Average latency (ms)
- Total sessions
- Last update timestamp

### Data Collection (from collector.py)

#### Metrics Collected Every 60s:

1. **Host Metrics** (via psutil):
   - CPU percent (total + per-core)
   - RAM percent + used/total MB
   - Disk percent + used/total GB
   - IO wait percentage
   - Network I/O (in/out MB)

2. **App Health** (via HTTP checks):
   - Status code (200, 404, 500, etc.)
   - Latency in ms
   - Error messages

3. **Container Status** (via Docker API):
   - Container name
   - Status (running only)
   - Restart count
   - Image tag

4. **Security Events** (via auth.log parsing):
   - SSH failed attempts
   - Event timestamps
   - Source IPs

5. **Port Scan** (via socket checks):
   - Open ports on localhost
   - Port descriptions

6. **Fail2Ban Status** (via CLI):
   - Banned IPs count

7. **OpenClaw Metrics** (via API):
   - Memory usage
   - Active sessions
   - Total sessions
   - Avg latency

### Database Schema (SQLite)

```sql
-- Host metrics
metrics_host:
  - timestamp
  - cpu_percent, cpu_per_core
  - ram_percent, ram_used_mb, ram_total_mb
  - disk_percent, disk_used_gb, disk_total_gb
  - io_wait
  - network_in_mb, network_out_mb

-- App health
metrics_apps:
  - timestamp
  - app_name
  - status_code
  - latency_ms
  - error_message

-- Docker containers
docker_containers:
  - timestamp
  - container_name
  - status
  - restart_count
  - image

-- Security events
security_events:
  - timestamp
  - event_type
  - source_ip
  - details

-- Port scan
port_scan:
  - timestamp
  - open_ports (JSON array)

-- Fail2Ban
fail2ban_status:
  - timestamp
  - banned_ips

-- Token usage
token_usage:
  - timestamp
  - provider
  - total_tokens
  - cost_usd

-- Tool usage
tool_usage:
  - timestamp
  - tool_name
  - usage_count

-- OpenClaw metrics
openclaw_metrics:
  - timestamp
  - memory_mb
  - active_sessions
  - total_sessions
  - avg_latency_ms
```

## Infrastructure Context

### Current Services (from docker-compose.yml)
```
127.0.0.1:9000  → Portainer (container management)
127.0.0.1:5678  → n8n (workflow automation)
127.0.0.1:6333  → Qdrant (vector memory DB)
127.0.0.1:8443  → Code-Server (browser IDE)
127.0.0.1:8501  → Overseer (current monitoring - TO BE REPLACED)
```

### Network Architecture
```
Internet → Cloudflare Access (SSO) → Cloudflare Tunnel → VPS (localhost) → Docker
```

### Key Constraints
- All services must bind to `127.0.0.1:PORT` for Cloudflared to reach them
- SSO via Cloudflare Access (Group: ZG, Users: fazaasro@gmail.com, gabriela.servitya@gmail.com)
- Security is religion - 4-layer defense is non-negotiable

## Requirements for Grafana Migration

### Must Preserve All Features
1. ✅ Real-time health checks for all services
2. ✅ Historical trends (24h+ retention)
3. ✅ Security monitoring (SSH, Fail2Ban, events)
4. ✅ Network/port monitoring
5. ✅ OpenClaw agent metrics
6. ✅ Token usage tracking
7. ✅ Tool usage analytics
8. ✅ Container status monitoring

### Must Enhance
1. **Scalability** - Should handle monitoring for:
   - AAC modules (Bag, Brain, Circle, Vessel)
   - Future services
   - Multi-instance deployments
2. **Alerting** - Proactive alerts for:
   - Service downtime
   - High CPU/RAM usage
   - Security events
   - Anomalies
3. **Custom Dashboards** - Easy to create module-specific views
4. **Integration** - Seamlessly integrate with:
   - Qdrant (metrics storage)
   - n8n (alert workflows)
   - OpenClaw (agent telemetry)

### Tech Stack Recommendations
- **Grafana** - Visualization and dashboards
- **Prometheus** - Metrics collection and storage
- **Node Exporter** - Host metrics (CPU, RAM, disk, network)
- **cAdvisor** - Docker container metrics
- **Loki** - Log aggregation (optional, for auth.log)
- **Alertmanager** - Alert routing and management
- **Blackbox Exporter** - HTTP health checks

## Success Criteria
- [ ] Grafana dashboard replaces Overseer completely
- [ ] All current features functional and improved
- [ ] Easy to add new services to monitor
- [ ] Alerts configured for critical metrics
- [ ] Data retention policy configured (24h+)
- [ ] Access control via Cloudflare Access
- [ ] Documentation for future expansions

## Next Steps
1. Evaluate current Overseer implementation (read all files in `/home/ai-dev/swarm/repos/overseer/`)
2. Design Grafana architecture
3. Create migration plan
4. Implement Grafana + Prometheus stack
5. Migrate all metrics and dashboards
6. Configure alerts
7. Test thoroughly
8. Update Cloudflare tunnel routing to new Grafana port
9. Document everything

---

*Use Kimi CLI for this task. Give it this full context before starting.*
