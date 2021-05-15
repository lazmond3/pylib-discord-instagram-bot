resource "aws_iam_role_policy" "cloudwatch_logs" {
  name = "cloudwatch_logs"
  role = aws_iam_role.ecs_task_execution_role.name

  policy = <<-EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:DescribeLogStreams",
                  "logs:PutLogEvents"
              ],
              "Resource": [
                  "${var.aws_cloudwatch_log_group_main_arn}"
              ]
          }
      ]    
  }
  EOF
}
