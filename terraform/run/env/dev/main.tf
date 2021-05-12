terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    bucket = "moikilo00-tfstate-bucket"
    key    = "discord-python-bot-lambda/dev.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "lambda-sample" {
  source   = "../../../module/lambda"
  app_name = var.app_name
}

output "base_url" {
  value = module.lambda-sample.base_url
}
