data "template_file" "container_definitions" {
  template = file(var.template_file_path)
  vars = {
    container_name       = var.container_name
    container_repository = var.container_repository
    container_tag        = var.container_tag
    # database_password    = var.aws_ssm_parameter_database_password_secret_arn
    # mysql_database       = var.task_mysql_database
    # mysql_user           = var.task_mysql_user

    # token = var.token
    # consumer_key = var.consumer_key
    # consumer_secret = var.consumer_secret
    # mid = var.mid
    # sessionid = var.sessionid
    aws_ssm_parameter_token_arn           = module.ssm.aws_ssm_parameter_token_arn
    aws_ssm_parameter_consumer_key_arn    = module.ssm.aws_ssm_parameter_consumer_key_arn
    aws_ssm_parameter_consumer_secret_arn = module.ssm.aws_ssm_parameter_consumer_secret_arn
    aws_ssm_parameter_mid_arn             = module.ssm.aws_ssm_parameter_mid_arn
    aws_ssm_parameter_sessionid_arn       = module.ssm.aws_ssm_parameter_sessionid_arn

    log_group = var.aws_cloudwatch_log_group_main_name
  }
}
