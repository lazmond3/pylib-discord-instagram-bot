data "template_file" "container_definitions" {
  template = file(var.template_file_path)
  vars = {
    container_name       = var.container_name
    container_repository = var.container_repository
    container_tag        = var.container_tag
    database_password    = var.aws_ssm_parameter_database_password_secret_arn
    mysql_database       = var.task_mysql_database
    mysql_user           = var.task_mysql_user
    # db_address           = var.task_db_address
    db_port   = var.task_db_port
    log_group = var.aws_cloudwatch_log_group_main_name
  }
}
