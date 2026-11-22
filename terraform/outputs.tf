output "alb_dns_name" {
  description = "Public DNS of the application load balancer"
  value       = aws_lb.app.dns_name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  value = aws_ecs_service.api.name
}

output "vpc_id" {
  value = aws_vpc.this.id
}
