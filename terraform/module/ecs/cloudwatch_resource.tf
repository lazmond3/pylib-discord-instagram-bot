resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/ecs/${var.app_name}"

  tags = {
    Name = "${var.app_name}"
  }

}
