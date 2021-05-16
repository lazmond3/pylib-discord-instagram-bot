resource "aws_security_group" "vpc_endpoint" {
  name   = "vpc_endpoint_sg"
  vpc_id = var.vpc_id

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    # cidr_blocks = [var.vpc_cidr] # 本当は 0.0.0.0 で設定してみてもいいけど
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }

  egress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    # cidr_blocks = [var.vpc_cidr]
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }
}
