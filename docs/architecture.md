# Architecture

Project1 is a sample production-style stack: a FastAPI service, reverse proxy, container runtime, CI/CD, AWS ECS infrastructure, and a Prometheus/Grafana observability plane.

```
                    ┌─────────────┐
  Clients ─────────►│    nginx    │ :8080 (local) / ALB :80 (AWS)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  FastAPI    │ /health /ready /items /metrics
                    └──────┬──────┘
                           │ scrape
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
     Prometheus      Alertmanager      Grafana
            ▲
            │
     node-exporter + cAdvisor
```

## Local vs cloud

| Layer | Local (Docker Compose) | AWS (Terraform) |
| --- | --- | --- |
| Compute | `app` container | ECS Fargate tasks |
| Ingress | nginx on port 8080 | Application Load Balancer |
| Network | `frontend`, `backend` (internal), `monitoring` | VPC with public/private subnets, NAT |
| Logs | stdout → `docker compose logs` | CloudWatch Logs |
| Metrics | Prometheus | Same stack can run on a bastion/ECS sidecar, or Amazon Managed Prometheus |

## Application

The API lives in `app/src/project1`. It exposes:

- `GET /health` — liveness
- `GET /ready` — readiness + uptime
- `GET /info` — version/env
- `GET/POST/DELETE /items` — in-memory demo resource (POST/DELETE require `X-API-Key` outside development)
- `GET /metrics` — Prometheus metrics (blocked at nginx for public clients)

State is in-memory on purpose so the demo stays easy to run. Replace `_items` with Postgres/Redis for a real workload.

## Security boundaries

- The API is not published directly; only nginx (local) or the ALB (AWS) is.
- `/metrics` is denied at nginx so scrape stays on the internal Docker network.
- Compose `backend` is an internal network: Prometheus can reach the API, the host cannot without a published port.
- ECS tasks sit in private subnets and accept traffic only from the ALB security group.
