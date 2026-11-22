terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.73"
    }
  }

  # Uncomment after creating a remote backend
  # backend "s3" {
  #   bucket = "project1-tfstate"
  #   key    = "infra/terraform.tfstate"
  #   region = "us-east-1"
  # }
}
