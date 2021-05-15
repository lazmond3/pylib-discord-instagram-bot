resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/ecs/${var.app_name}"

  tags = {
    Name = "${var.app_name}"
  }

}

# # デバッグ用 python2
# resource "aws_cloudwatch_log_group" "python2" {
#   name = "/aws/ecs/${var.app_name}/python2"

#   tags = {
#     Name = "linebot2-python2"
#   }
# }

# # デバッグ用 app2
# resource "aws_cloudwatch_log_group" "app2" {
#   name = "/aws/ecs/${var.app_name}/app2"
#   # name = "/aws/ecs/python2"

#   tags = {
#     Name = "linebot2-app2"
#   }
# }
