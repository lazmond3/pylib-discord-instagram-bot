# SecurityGroup
# https://www.terraform.io/docs/providers/aws/r/security_group.html
# ECS に対してではなく VPC に対する セキュリティグループでは？
# とおもったら、 ecs-service と、 aws_lb に対して制限している

resource "aws_security_group" "ecs" {
  name        = "${var.app_name}-ecs"
  description = "handson ecs"

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
    Name = "${var.app_name}-ecs"
  }

  # これは必要. これがないとサービス動かなくなる
  # これ、  RDS からの返却を使うために、全部をオープンにする
  # debug
  # => 無駄だった, 結果変わらず
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
