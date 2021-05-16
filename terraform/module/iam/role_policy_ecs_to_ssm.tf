resource "aws_iam_role_policy" "ecs_to_ssm" {
  name  = "ecs_to_ssm"
  count = length(var.secret_arns)

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
          "${var.secret_arns[count.index]}"
        ]
      }
    ]
  }
  EOF
}
