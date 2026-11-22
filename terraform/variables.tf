variable "aws_region" {
  type        = string
  description = "AWS region for all resources"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  default     = "project1"
}

variable "environment" {
  type        = string
  default     = "staging"
}

variable "vpc_cidr" {
  type    = string
  default = "10.42.0.0/16"
}

variable "container_image" {
  type        = string
  default     = ""
  description = "Full image URI. Empty uses the ECR repo created here with tag latest."
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "desired_count" {
  type    = number
  default = 2
}

variable "cpu" {
  type    = number
  default = 256
}

variable "memory" {
  type    = number
  default = 512
}

variable "api_key" {
  type        = string
  sensitive   = true
  description = "API key injected into the container"
}
