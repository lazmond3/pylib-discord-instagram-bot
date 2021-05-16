# https://yyh-gl.github.io/tech-blog/blog/terraform_ecs/
# SSM Parameter data source
# # https://www.terraform.io/docs/providers/aws/d/ssm_parameter.html
# resource "aws_ssm_parameter" "database_name" {
#   name  = "MYSQL_DATABASE"
#   type  = "String"
#   value = "MYSQL_DATABASE"
# }


# 【解説】locals は名前のとおりローカル変数です。
# variables だと `${}` 展開できないのでこちらを使用しました。
# 他にやり方があれば教えてほしいです。
locals {
  name = "${var.app_name}-rds-mysql"
}

resource "aws_db_subnet_group" "this" {
  name        = local.name
  description = local.name
  subnet_ids  = var.aws_lb_private_ids
}

# RDS Cluster
# https://www.terraform.io/docs/providers/aws/r/rds_cluster.html
resource "aws_rds_cluster" "this" {
  cluster_identifier = local.name

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = ["${aws_security_group.rds.id}"]

  engine = "aurora-mysql"
  port   = "3306"

  #   database_name   = aws_ssm_parameter.database_name.value
  database_name = var.mysql_database
  #   master_username = aws_ssm_parameter.database_user.value
  master_username = var.mysql_user
  master_password = var.mysql_password

  # RDSインスタンス削除時のスナップショットの取得強制を無効化
  skip_final_snapshot = true

  # 使用する Parameter Group を指定
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.this.name
}

# RDS Cluster Instance
# https://www.terraform.io/docs/providers/aws/r/rds_cluster_instance.html
resource "aws_rds_cluster_instance" "this" {
  identifier         = local.name
  cluster_identifier = aws_rds_cluster.this.id

  engine = "aurora-mysql"

  instance_class = "db.t3.small"
}

# RDS Cluster Parameter Group
# https://www.terraform.io/docs/providers/aws/r/rds_cluster_parameter_group.html
# 日本時間に変更 & 日本語対応のために文字コードを変更
resource "aws_rds_cluster_parameter_group" "this" {
  name   = local.name
  family = "aurora-mysql5.7"

  parameter {
    name  = "time_zone"
    value = "Asia/Tokyo"
  }

  parameter {
    name  = "character_set_client"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_connection"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_database"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_results"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }
}

# terraform applyコマンド完了時にコンソールにエンドポイントを表示
# 【解説】もしエンドポイントも機密情報として扱うのであれば
# ここで表示されたエンドポイントをパラメータストアに格納すればよい。
# 今回は紹介のために使用。
output "rds_endpoint" {
  value = aws_rds_cluster.this.endpoint
}
