terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    bucket = "discord-python-bot-lambda"
    key    = "discord-python-bot-lambda/tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "vpc" {
  source                   = "../../../module/vpc"
  app_name                 = var.app_name
  vpc_azs                  = var.vpc_azs
  vpc_cidr                 = var.vpc_cidr
  vpc_public_subnet_cidrs  = var.vpc_public_subnet_cidrs
  vpc_private_subnet_cidrs = var.vpc_private_subnet_cidrs
}

module "alb" {
  source            = "../../../module/alb"
  aws_lb_public_ids = module.vpc.vpc_aws_subnet_public_ids
  app_name          = var.app_name
  vpc_id            = module.vpc.vpc_id
  cert_arn          = var.cert_arn
  sg_alb_id         = module.security.sg_alb_id
}

module "security" {
  source   = "../../../module/security"
  vpc_id   = module.vpc.vpc_id
  app_name = var.app_name
}

module "route53" {
  source                    = "../../../module/route53"
  app_domain                = var.app_domain
  cert_route53_zone_main_id = var.cert_route53_zone_main_id
  alb_dns_name              = module.alb.alb_dns_name
  alb_zone_id               = module.alb.alb_zone_id
}

module "ecr" {
  source   = "../../../module/ecr"
  ecr_name = var.ecr_name
}

# ここまで実装した
# module "vpc_endpoint" {
#   source                                  = "../../../module/vpc_endpoint"
#   vpc_id                                  = module.vpc.vpc_id
#   vpc_cidr                                = var.vpc_cidr
#   vpc_aws_subnet_private_ids              = module.vpc.vpc_aws_subnet_private_ids
#   vpc_aws_route_table_id_for_private_list = module.vpc.vpc_aws_route_table_id_for_private_list
# }


# ここまで実装した
# -------------------------------------------
module "cloudwatch" {
  source   = "../../../module/cloudwatch"
  app_name = var.app_name
}
module "ecs" {
  source                       = "../../../module/ecs"
  app_name                     = var.app_name
  template_file_path           = var.template_file_path
  ecs_load_balancer_target_arn = module.alb.alb_target_group_main_arn
  ecs_subnets                  = module.vpc.vpc_aws_subnet_public_ids
  container_name               = var.container_name
  container_port               = var.container_port
  container_repository         = var.container_repository
  container_tag                = var.container_tag

  aws_ssm_parameter_token_arn           = module.ssm.aws_ssm_parameter_token_arn
  aws_ssm_parameter_consumer_key_arn    = module.ssm.aws_ssm_parameter_consumer_key_arn
  aws_ssm_parameter_consumer_secret_arn = module.ssm.aws_ssm_parameter_consumer_secret_arn
  aws_ssm_parameter_mid_arn             = module.ssm.aws_ssm_parameter_mid_arn
  aws_ssm_parameter_sessionid_arn       = module.ssm.aws_ssm_parameter_sessionid_arn

  # token = var.token
  # consumer_key = var.consumer_key
  # consumer_secret = var.consumer_secret
  # mid = var.mid
  # sessionid = var.sessionid

  aws_ecr_repository_name = module.ecr.aws_ecr_repository_name
  # aws_ssm_parameter_database_password_secret_arn = module.ssm.aws_ssm_parameter_database_password_secret_arn
  aws_cloudwatch_log_group_main_name = module.cloudwatch.aws_cloudwatch_log_group_main_name
  task_mysql_database                = var.task_mysql_database
  task_mysql_user                    = var.task_mysql_user
  # task_db_address                                = module.rds.db_address
  task_db_port                = var.task_db_port
  aws_security_group_ecs_id   = module.security.aws_security_group_ecs_id
  ecs_task_execution_role_arn = module.iam.ecs_task_execution_role_arn
}

module "iam" {
  source                            = "../../../module/iam"
  app_name                          = var.app_name
  vpc_id                            = module.vpc.vpc_id
  aws_cloudwatch_log_group_main_arn = module.cloudwatch.aws_cloudwatch_log_group_main_arn
  # aws_ssm_parameter_database_password_secret_arn = module.ssm.aws_ssm_parameter_database_password_secret_arn
  ecs_task_execution_role_id = module.iam.aws_iam_role_ecs_task_execution_role_id
  secret_arns = [
    module.ssm.aws_ssm_parameter_token_arn,
    module.ssm.aws_ssm_parameter_consumer_key_arn,
    module.ssm.aws_ssm_parameter_consumer_secret_arn,
    module.ssm.aws_ssm_parameter_mid_arn,
    module.ssm.aws_ssm_parameter_sessionid_arn
  ]
}

module "ssm" {
  source          = "../../../module/ssm"
  token           = var.token
  consumer_key    = var.consumer_key
  consumer_secret = var.consumer_secret
  mid             = var.mid
  sessionid       = var.sessionid
}


# 動画用 s3
resource "aws_s3_bucket" "discord-python-video" {
  bucket = "discord-python-video"
  acl    = "public-read"

  versioning {
    enabled = true
  }
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    # max_age_seconds = 3000
  }

  tags = {
    Name        = "discord-python-video"
    Environment = "Dev"
  }
}
