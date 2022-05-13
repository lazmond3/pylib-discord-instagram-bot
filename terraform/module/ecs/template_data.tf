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
    token_arn           = var.aws_ssm_parameter_token_arn
    consumer_key_arn    = var.aws_ssm_parameter_consumer_key_arn
    consumer_secret_arn = var.aws_ssm_parameter_consumer_secret_arn
    mid_arn             = var.aws_ssm_parameter_mid_arn
    sessionid_arn       = var.aws_ssm_parameter_sessionid_arn

    aws_access_key_id_arn     = var.aws_ssm_parameter_aws_access_key_id_arn
    aws_secret_access_key_arn = var.aws_ssm_parameter_aws_secret_access_key_arn

    aws_secret_es_host_arn      = var.aws_ssm_parameter_es_host_arn
    aws_secret_es_user_name_arn = var.aws_ssm_parameter_es_user_name_arn
    aws_secret_es_password_arn  = var.aws_ssm_parameter_es_password_arn
    env              = var.env

    log_group = var.aws_cloudwatch_log_group_main_name
  }
}
