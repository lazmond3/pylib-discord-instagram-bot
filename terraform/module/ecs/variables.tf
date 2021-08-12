variable "app_name" {
  type = string
}

variable "template_file_path" {
  type = string
}

variable "ecs_desired_count" {
  default = "1"
}


# ecs cluster
# vpc からもらう
# private にするのが普通
variable "ecs_subnets" {
  type = list(string) # aws_subnet.privates.*.id
}

# task 定義
variable "container_name" {
  type = string
}
variable "container_port" {
  type = string
}

variable "container_repository" {
  type = string
}

variable "container_tag" {
  type = string
}

# ECS の秘密パラメータ
variable "aws_ssm_parameter_token_arn" {
  type = string
}
variable "aws_ssm_parameter_consumer_key_arn" {
  type = string
}
variable "aws_ssm_parameter_consumer_secret_arn" {
  type = string
}
variable "aws_ssm_parameter_mid_arn" {
  type = string
}
variable "aws_ssm_parameter_sessionid_arn" {
  type = string
}
variable "aws_ssm_parameter_aws_access_key_id_arn" {
  type = string
}
variable "aws_ssm_parameter_aws_secret_access_key_arn" {
  type = string
}

# variable "token" {
#   type = string
# }
# # discord の キー
# variable "consumer_key" {
#   type = string
# }
# variable "consumer_secret" {
#   type = string
# }
# variable "mid" {
#   type = string
# }
# variable "sessionid" {
#   type = string
# }

variable "aws_ecr_repository_name" {
  type = string
}
# variable "aws_ssm_parameter_database_password_secret_arn" {
#   type = string
# }

variable "aws_cloudwatch_log_group_main_name" {
  type = string
}
variable "task_mysql_database" {
  type = string
}
variable "task_mysql_user" {
  type = string
}
# variable "task_db_address" {
#   type = string
# }
variable "task_db_port" {
  type = string
}


# security 
variable "aws_security_group_ecs_id" {
  type = string
}

variable "ecs_task_execution_role_arn" {
  type = string
}
