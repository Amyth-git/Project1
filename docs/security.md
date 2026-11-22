# Security

This project applies a small set of defaults that are appropriate for a student/demo handover and a starting point for production.

## Container

- Multi-stage image, slim Python base, no compilers in the runtime stage
- Non-root `app` user
- Read-only root filesystem with `tmpfs` for `/tmp`
- `no-new-privileges`
- CPU/memory limits on the API
- Image scan on CI (Trivy) and ECR `scan_on_push`

## Network

- Public clients talk to nginx or the ALB only
- `/metrics` is not exposed through nginx
- Compose `backend` network is internal
- ECS tasks have no public IP; egress goes through NAT
- ALB security group is the only ingress to the task port

## Application

- Mutating endpoints require `X-API-Key` when `APP_ENV` is not `development`
- CORS is closed in production (`allow_origins=[]`)
- nginx hides version tokens and adds baseline headers
- Request rate limiting at nginx (`10r/s`, burst 20)

## Secrets

- Never commit `.env` or `terraform.tfvars`
- `API_KEY` and Grafana password come from environment variables
- GitHub Actions uses repository secrets for AWS keys
- Terraform marks `api_key` sensitive (still consider AWS Secrets Manager for production)

## What to add next

- TLS on the ALB (ACM certificate) and redirect HTTP → HTTPS
- OIDC for GitHub → AWS (drop long-lived access keys)
- WAF on the ALB
- Secrets Manager + ECS secret injection instead of plain environment variables
- Network policies / AWS VPC endpoints for ECR and CloudWatch
