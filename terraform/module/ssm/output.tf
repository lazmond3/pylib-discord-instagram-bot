output "aws_ssm_parameter_token_arn" {
  value = aws_ssm_parameter.token.arn
}
output "aws_ssm_parameter_consumer_key_arn" {
  value = aws_ssm_parameter.consumer_key.arn
}
output "aws_ssm_parameter_consumer_secret_arn" {
  value = aws_ssm_parameter.consumer_secret.arn
}
output "aws_ssm_parameter_mid_arn" {
  value = aws_ssm_parameter.mid.arn
}
output "aws_ssm_parameter_sessionid_arn" {
  value = aws_ssm_parameter.sessionid.arn
}
output "aws_ssm_parameter_aws_access_key_id_arn" {
  value = aws_ssm_parameter.v_aws_access_key_id.arn
}
output "aws_ssm_parameter_aws_secret_access_key_arn" {
  value = aws_ssm_parameter.v_aws_secret_access_key.arn
}
output "aws_ssm_parameter_es_host" {
  value = aws_ssm_parameter.es_host.arn
}
output "aws_ssm_parameter_es_user_name" {
  value = aws_ssm_parameter.es_user_name.arn
}
output "aws_ssm_parameter_es_password" {
  value = aws_ssm_parameter.es_password.arn
}
