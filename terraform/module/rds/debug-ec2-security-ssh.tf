resource "aws_security_group" "ec2_public_bastian" {
  name   = "ec2_bastian"
  vpc_id = var.vpc_id

  ingress {
    # from_port   = 22
    # to_port     = 22
    # protocol    = "tcp"
    # cidr_blocks = [var.vpc_cidr] # 本当は 0.0.0.0 で設定してみてもいいけど
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }

  egress {
    # from_port   = 0
    # to_port     = 0
    # protocol    = "tcp"
    # cidr_blocks = [var.vpc_cidr]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }
}

resource "aws_security_group" "ec2_private" {
  name   = "ec2_private"
  vpc_id = var.vpc_id

  # ingress {
  #   from_port   = 22
  #   to_port     = 22
  #   protocol    = "tcp"
  #   cidr_blocks = [var.vpc_cidr] # 本当は 0.0.0.0 で設定してみてもいいけど
  # }
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }

  egress {
    # from_port   = 0
    # to_port     = 0
    # protocol    = "tcp"
    # cidr_blocks = [var.vpc_cidr]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }
}

resource "aws_security_group" "ec2_private_nat_to_global" {
  name   = "ec2_private_nat_to_global"
  vpc_id = var.vpc_id

  ingress {
    # from_port   = 0
    # to_port     = 65535
    # protocol    = "tcp"
    # cidr_blocks = ["10.0.0.0/16"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }

  egress {
    # from_port   = 0
    # to_port     = 65535
    # protocol    = "tcp"
    # cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
  }
}

resource "aws_security_group" "mysql_to_private" {
  name   = "mysql_to_private"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # 本当は 0.0.0.0 で設定してみてもいいけど
    # from_port   = 3306
    # to_port     = 3306
    # protocol    = "tcp"
    # cidr_blocks = [var.vpc_cidr] # 本当は 0.0.0.0 で設定してみてもいいけど
  }
}
