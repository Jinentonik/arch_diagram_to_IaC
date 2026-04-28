variable "region" {
  type    = string
  default = "us-east-1" # Replace with the default region you want to use
}

terraform {
  backend "s3" {
    bucket         = "jktan-s3-state-file"
    key            = "global/diagram-to-code/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    profile        = "diagram-to-code"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider


provider "aws" {
  profile = "diagram-to-code"
  region  = var.region
}