terraform {

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.30.0"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

locals {
  service_name = "denis-telebot"
}

module "denis-telebot-lambda" {
  source = "./modules/denis-telebot"
  service_name = local.service_name
  region = var.region
}