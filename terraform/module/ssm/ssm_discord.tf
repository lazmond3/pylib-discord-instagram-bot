resource "aws_ssm_parameter" "token" {
  name  = "token"
  type  = "String"
  value = var.token
}

resource "aws_ssm_parameter" "consumer_key" {
  name  = "consumer_key"
  type  = "String"
  value = var.consumer_key
}

resource "aws_ssm_parameter" "consumer_secret" {
  name  = "consumer_secret"
  type  = "String"
  value = var.consumer_secret
}
resource "aws_ssm_parameter" "mid" {
  name  = "mid"
  type  = "String"
  value = var.mid
}
resource "aws_ssm_parameter" "sessionid" {
  name  = "sessionid"
  type  = "String"
  value = var.sessionid
}
resource "aws_ssm_parameter" "v_aws_access_key_id" {
  name  = "v_aws_access_key_id"
  type  = "String"
  value = var.aws_access_key_id
}
resource "aws_ssm_parameter" "v_aws_secret_access_key" {
  name  = "v_aws_secret_access_key"
  type  = "String"
  value = var.aws_secret_access_key
}

resource "aws_ssm_parameter" "es_host" {
  name  = "es_host"
  type  = "String"
  value = var.es_host
}
resource "aws_ssm_parameter" "es_user_name" {
  name  = "es_user_name"
  type  = "String"
  value = var.es_host
}
resource "aws_ssm_parameter" "es_password" {
  name  = "es_user_name"
  type  = "String"
  value = var.es_password
}
