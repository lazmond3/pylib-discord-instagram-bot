resource "aws_iam_role_policy" "ecs_to_ssm" {
  name = "ecs_to_ssm"
  role = var.ecs_task_execution_role_id

  policy = jsonencode({
    Version = "2021-10-17"
    Statement = [
      {
        Action = [
          "ssm:GetParameters"
        ]
        EFfect   = "Allow"
        Resource = var.secret_arns
      }
    ]
  })

  # <<-EOF
  # {
  #   "Version": "2012-10-17",
  #   "Statement": [
  #     {
  #       "Action": [
  #         "ssm:GetParameters"
  #       ],
  #       "Effect": "Allow",
  #       "Resource": [
  #         "${var.secret_arns[count.index]}"
  #       ]
  #     }
  #   ]
  # }
  # EOF
}
