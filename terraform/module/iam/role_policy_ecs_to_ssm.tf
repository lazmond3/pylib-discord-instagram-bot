resource "aws_iam_role_policy" "ecs_to_ssm" {
  name = "ecs_to_ssm"
  role = var.ecs_task_execution_role_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ssm:GetParameters"
        ]
        Effect   = "Allow"
        Resource = var.secret_arns
      },
      {
        Action = [
          "ssm:DescribeParameters"
        ]
        Effect   = "Allow"
        Resource = "*"
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
