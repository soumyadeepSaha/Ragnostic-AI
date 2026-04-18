# 📊 Prometheus Monitoring Setup - Complete Guide

## ✅ What Was Done For You

### 1. **prometheus.yml Configuration** ✅
- Configured to scrape Gateway metrics (port 3000)
- Configured to scrape Agents Service metrics (port 8000)
- 15-second scrape interval for real-time monitoring

### 2. **Gateway Metrics** ✅
- Already had `prom-client` installed
- `/metrics` endpoint already configured
- Tracking request counts and durations

### 3. **Agents Service Metrics** ✅
- Added Prometheus middleware to `main.py`
- `/metrics` endpoint now available
- Tracking request counts and durations per endpoint
- `prometheus-client` package installed

### 4. **Prometheus Binary** (In Progress...)
- Downloading Prometheus 2.51.1
- Will be installed to `C:\prometheus`

---

## 📋 Next Steps

### Step 1: Wait for Prometheus Download ⏳

The setup script is downloading Prometheus (it's ~50MB, takes a few minutes).

When complete, you'll see:
```
✅ Prometheus installed at: C:\prometheus
Setup complete! Run Prometheus with:
```

### Step 2: Start Prometheus

```bash
cd C:\prometheus
.\prometheus.exe --config.file=C:\Users\dante\Desktop\Ragnostic-AI\prometheus.yml
```

Or create a batch file `run_prometheus.bat`:
```batch
@echo off
cd C:\prometheus
.\prometheus.exe --config.file=C:\Users\dante\Desktop\Ragnostic-AI\prometheus.yml
```

### Step 3: Access Prometheus Dashboard

Open browser:
```
http://localhost:9090
```

### Step 4: View Metrics

In Prometheus UI:
- Search for: `agent_requests_total` (requests to agents)
- Search for: `agent_request_duration_seconds` (response times)
- Search for: `requests_total` (gateway requests)

---

## 🎯 Metrics Available

### Gateway Metrics (Port 3000)
```
requests_total - Total requests to gateway
```

### Agents Service Metrics (Port 8000)
```
agent_requests_total{endpoint="/planner/"} - Planner requests
agent_requests_total{endpoint="/reason/"} - Reasoning requests
agent_requests_total{endpoint="/retrieve/"} - Retrieval requests
agent_requests_total{endpoint="/verify/"} - Verification requests
agent_requests_total{endpoint="/tool/"} - Tool requests
agent_requests_total{endpoint="/mcp"} - MCP requests

agent_request_duration_seconds - Response time per endpoint
```

---

## 📊 Example Queries

### Total Requests to Each Agent
```promql
agent_requests_total
```

### Average Response Time
```promql
rate(agent_request_duration_seconds_sum[5m]) / rate(agent_request_duration_seconds_count[5m])
```

### Requests Per Second
```promql
rate(requests_total[1m])
```

### Error Rate (if errors tracked)
```promql
rate(agent_errors_total[5m])
```

---

## 🚀 Services Status

### Running Services
- ✅ FastAPI on port 8000 (with /metrics)
- ✅ Gateway on port 3000 (with /metrics)
- ⏳ Prometheus (downloading)

### Metrics Endpoints
- `http://localhost:8000/metrics` - Agent metrics
- `http://localhost:3000/metrics` - Gateway metrics
- `http://localhost:9090/` - Prometheus dashboard

---

## 🔧 Configuration File

**File:** `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agents-service'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
  
  - job_name: 'gateway'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: '/metrics'
```

---

## 📈 What You Can Monitor

1. **Request Volume** - How many requests each agent gets
2. **Response Times** - Performance of each agent
3. **Error Rates** - Track failures
4. **System Health** - Uptime and availability
5. **Traffic Patterns** - Peak times and usage

---

## 💡 Pro Tips

### View Real-Time Metrics Without Dashboard
```bash
# Get raw metrics from agents service
curl http://localhost:8000/metrics

# Get raw metrics from gateway
curl http://localhost:3000/metrics
```

### Create Alerts
In Prometheus, you can set up alerts for:
- High response times
- Too many errors
- Service down
- High memory usage

### Graph Metrics
Prometheus has built-in graphing:
1. Go to http://localhost:9090
2. Type query: `agent_requests_total`
3. Click "Graph" tab
4. Adjust time range

---

## ✨ Next: Advanced Setup (Optional)

### Add Grafana for Better Dashboards
```bash
docker run -d -p 3001:3000 grafana/grafana
# Then connect Prometheus as data source
```

### Add Alerting
Create `alerts.yml` with alert rules and restart Prometheus

### Export Metrics to External Service
Configure remote_write in prometheus.yml to send metrics to:
- InfluxDB
- Google Cloud Monitoring
- Datadog
- New Relic

---

## ❓ Troubleshooting

### Metrics endpoint returns 404
- Check if service is running
- Make sure you restarted the service after code changes

### Prometheus can't connect to targets
- Verify services are running on correct ports
- Check firewall settings
- Verify /metrics endpoint responds with curl

### Prometheus UI not loading
- Check port 9090 is not blocked
- Make sure prometheus.exe started successfully

---

## 📝 Commands to Remember

```bash
# Download and install Prometheus (already running)
powershell -ExecutionPolicy Bypass -File setup_prometheus.ps1

# Run Prometheus
cd C:\prometheus
.\prometheus.exe --config.file=prometheus.yml

# Check metrics (from project root)
curl http://localhost:8000/metrics
curl http://localhost:3000/metrics

# Access dashboard
http://localhost:9090
```

---

**Status: Prometheus installation in progress! Check back soon.** ⏳
