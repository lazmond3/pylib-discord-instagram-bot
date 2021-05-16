resource "aws_lb_listener" "http_to_https" {
  port     = "80"
  protocol = "HTTP"

  load_balancer_arn = aws_lb.this.arn

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  port     = "443"
  protocol = "HTTPS"

  certificate_arn = var.cert_arn

  load_balancer_arn = aws_lb.this.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.id
  }
}
