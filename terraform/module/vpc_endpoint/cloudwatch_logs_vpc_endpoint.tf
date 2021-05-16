# # ECS から cloudwatch にアクセスするために必要なVPCエンドポイント
# resource "aws_vpc_endpoint" "cloudwatch" {
#   vpc_id              = var.vpc_id
#   service_name        = "com.amazonaws.ap-northeast-1.monitoring"
#   vpc_endpoint_type   = "Interface"
#   subnet_ids          = var.aws_subnet_private_ids
#   security_group_ids  = [aws_security_group.vpc_endpoint.id]
#   private_dns_enabled = true
# }


# ECS から cloudwatch にアクセスするために必要なVPCエンドポイント
resource "aws_vpc_endpoint" "cloudwatch_logs" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.ap-northeast-1.logs"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.vpc_aws_subnet_private_ids
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true
}
