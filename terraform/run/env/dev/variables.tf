variable "app_name" {
  type = string
}

# route53, cert
variable "root_domain" {
  type = string
}
variable "app_domain" {
  type = string
}

# vpc 用の variables
variable "vpc_cidr" {
  default = "10.0.0.0/16"
}
variable "vpc_azs" {
  type = list(string)
  # default = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
}

variable "vpc_public_subnet_cidrs" {
  type = list(string)
  # default = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
}

variable "vpc_private_subnet_cidrs" {
  type = list(string)
  # default = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
}


# variable "project_name_app" {
#   type = string
# }
variable "ecr_name" {
  type = string
}
# variable "project_name_bot_server" {
#   type = string
# }


variable "template_file_path" {
  type = string
}

variable "container_repository" {
  type = string
}
variable "container_name" {
  type = string
}
variable "container_port" {
  type = string
}

variable "container_tag" {
  type = string
}

# # secret
# ## これは secret じゃない
variable "task_mysql_database" {
  type = string
}
variable "task_mysql_user" {
  type = string
}

variable "task_db_port" {
  type = string
}

# TF_VAR_mysql_password で渡す
# variable "mysql_password" {
#   type = string
# }

# ECS のパラメータ
variable "token" {
  type = string
}
# discord の キー
variable "consumer_key" {
  type = string
}
variable "consumer_secret" {
  type = string
}
variable "mid" {
  type = string
}
variable "sessionid" {
  type = string
}

# cert
variable "cert_arn" {
  type = string
}

variable "cert_route53_zone_main_id" {
  type = string
}


# boto3 用 の環境変数
variable "aws_access_key_id" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}
