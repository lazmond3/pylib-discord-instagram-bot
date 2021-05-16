# SecurityGroup
# https://www.terraform.io/docs/providers/aws/r/security_group.html
# ECS に対してではなく VPC に対する セキュリティグループでは？
# とおもったら、 ecs-service と、 aws_lb に対して制限している

resource "aws_security_group" "alb" {
  name        = "${var.app_name}-alb-2"
  description = "alb"

  # セキュリティグループを配置するVPC
  vpc_id = var.vpc_id

  # セキュリティグループ内のリソースからインターネットへのアクセス許可設定
  # 今回の場合DockerHubへのPullに使用する。
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-alb-2"
  }

  # これは必要. これがないとサービス動かなくなる
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    # 同一VPC内からのアクセスのみ許可
    # cidr_blocks = ["10.0.0.0/16"]
    cidr_blocks = ["0.0.0.0/0"]
  }
}
