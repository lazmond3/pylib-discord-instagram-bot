variable "app_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "aws_cloudwatch_log_group_main_arn" {
  type = string
}

variable "aws_ssm_parameter_database_password_secret_arn" {
  type = string
}

variable "ecs_task_execution_role_id" {
  type = string
}