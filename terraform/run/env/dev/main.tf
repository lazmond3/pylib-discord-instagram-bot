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

# module "lambda-sample" {
#   source   = "../../../module/lambda"
#   app_name = var.app_name
# }

module "vpc" {
  source   = "../../../module/vpc"
  app_name = var.app_name
}

module "ecr" {
  source                         = "../../../module/ecr"
  app_name                       = var.app_name
  ecr-name                       = var.ecr-name
  vpc_id                         = module.vpc.vpc_id
  aws_route_table_ids_for_public = module.vpc.aws_route_table_ids_for_public
  vpc_cidr                       = module.vpc.vpc_cidr

}