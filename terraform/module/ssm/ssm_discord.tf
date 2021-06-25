resource "aws_ssm_parameter" "token" {
  name  = "token"
  type  = "String"
  value = var.token # TODO: FIX これTF_VAR_由来にしたい.
}

resource "aws_ssm_parameter" "consumer_key" {
  name  = "consumer_key"
  type  = "String"
  value = var.consumer_key # TODO: FIX これTF_VAR_由来にしたい.
}

resource "aws_ssm_parameter" "consumer_secret" {
  name  = "consumer_secret"
  type  = "String"
  value = var.consumer_secret # TODO: FIX これTF_VAR_由来にしたい.
}
resource "aws_ssm_parameter" "mid" {
  name  = "mid"
  type  = "String"
  value = var.mid # TODO: FIX これTF_VAR_由来にしたい.
}
resource "aws_ssm_parameter" "sessionid" {
  name  = "sessionid"
  type  = "String"
  value = var.sessionid # TODO: FIX これTF_VAR_由来にしたい.
}
resource "aws_ssm_parameter" "v_aws_access_key_id" {
  name  = "v_aws_access_key_id"
  type  = "String"
  value = var.aws_access_key_id # TODO: FIX これTF_VAR_由来にしたい.
}
resource "aws_ssm_parameter" "v_aws_secret_access_key" {
  name  = "v_aws_secret_access_key"
  type  = "String"
  value = var.aws_secret_access_key # TODO: FIX これTF_VAR_由来にしたい.
}
