resource "aws_iam_role_policy" "mysql_db_password_policy_secretsmanager" {
  name = "password-policy-mysql_db_password_policy_secretsmanager"
  role = var.ecs_task_execution_role_id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ssm:GetParameters"
        ],
        "Effect": "Allow",
        "Resource": [
          "${var.aws_ssm_parameter_database_password_secret_arn}"
        ]
      }
    ]
  }
  EOF
}
