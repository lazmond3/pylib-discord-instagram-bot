resource "aws_ssm_parameter" "database_password_secret" {
  name  = "MYSQL_PASSWORD"
  type  = "String"
  value = var.mysql_password # TODO: FIX これTF_VAR_由来にしたい.
}
