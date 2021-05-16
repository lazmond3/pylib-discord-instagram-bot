variable "app_name" {
  type = string
}
variable "vpc_id" {
  type = string
}

variable "aws_lb_public_ids" {
  type = list(string)
}
variable "aws_lb_private_ids" {
  type = list(string)
}
variable "vpc_cidr" {
  type = string
}
# variable "debug_ec2_aws_route_table_id_0" {
#   type = string
# }
variable "mysql_database" {
  type = string
}

variable "ecs_task_execution_role_id" {
  type = string
}

# TF_VAR_mysql_password で渡す
variable "mysql_password" {
  type = string
}
variable "mysql_user" {
  type = string
}
