

# ここで初めて ELB(ALB?) を 定義できる。 DNS名とかいってたアレはなんだったんだ
# ELB Target Group
# https://www.terraform.io/docs/providers/aws/r/lb_target_group.html
# ALB で定義できるのは、ターゲットグループの定義 すなわちVPCのこと。(forward) 先に指定できる)
# 逆にCloudFront などはredirectじゃないと指定できない気がするけど、その場合画像ファイルとかうまく表示できなくなるのでは？
resource "aws_lb_target_group" "main" {
  name = var.app_name

  # ターゲットグループを作成するVPC
  # これ雑じゃない？ どのサブネットに渡すとか
  # どの VPC に渡すか、だけでいいのか？
  vpc_id = var.vpc_id

  # ALBからECSタスクのコンテナへトラフィックを振り分ける設定
  # application load balancer ? 
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"

  # コンテナへの死活監視設定
  health_check {
    port = 8080
    path = "/hello"
  }
}

# 単純なリダイレクトなので、 LISTENER_RULE が不要

resource "aws_lb" "this" {
  load_balancer_type = "application"
  name               = var.app_name

  security_groups = [var.sg_alb_id]
  # security_groups = [aws_security_group.alb.id]
  subnets = var.aws_lb_public_ids
}
