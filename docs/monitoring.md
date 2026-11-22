# Monitoring

## Components

| Service | URL (local) | Role |
| --- | --- | --- |
| Prometheus | http://localhost:9090 | Scrapes API, node, and container metrics; evaluates alerts |
| Alertmanager | http://localhost:9093 | Groups and routes alerts |
| Grafana | http://localhost:3000 | Dashboards (admin / `GRAFANA_ADMIN_PASSWORD`) |
| cAdvisor | http://localhost:8081 | Container CPU/memory/filesystem |
| node-exporter | http://localhost:9100 | Host metrics |

Grafana is provisioned automatically: Prometheus is the default datasource, and **Project1 Overview** is loaded from `monitoring/grafana/dashboards/app-overview.json`.

## Metrics

The API uses `prometheus-fastapi-instrumentator`. After traffic you should see series such as:

- `http_requests_total`
- `http_request_duration_seconds_bucket`
- `up{job="project1-api"}`

Generate sample traffic:

```bash
for i in $(seq 1 50); do curl -s -o /dev/null http://localhost:8080/health; done
curl -s http://localhost:8080/items
```

Then open Grafana → Project1 → Project1 Overview.

## Alerts

Defined in `monitoring/prometheus/alerts.yml`:

- **ServiceDown** — API scrape target missing
- **HighErrorRate** — 5xx share > 5% for 5 minutes
- **HighLatency** — p95 > 750ms for 10 minutes
- **HostHighCPU** / **HostLowDisk**
- **ContainerRestarting**

Alertmanager ships to a placeholder webhook. Point `receivers` at Slack/PagerDuty by setting a real URL in `monitoring/alertmanager/alertmanager.yml`.

## Cloud

ECS Container Insights is enabled on the cluster. Application logs go to `/ecs/project1-<env>`. For a cloud-native Prometheus, swap the scrape config to Amazon Managed Prometheus or run this same Compose monitoring profile on a dedicated ops instance.
