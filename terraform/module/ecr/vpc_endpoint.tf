resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.ap-northeast-1.ecr.dkr"
  vpc_endpoint_type = "Interface"
  #The ID of one or more subnets in which to create a network interface for the endpoint.
  # その中にネットワークインターフェース(VPCエンドポイント)を作るためのサブネットのID
  # プライベートサブネットに外部ヘ行く道がなくて困っているので、VPCエンドポイントを作成する？
  #Applicable for endpoints of type GatewayLoadBalancer and Interface.

  subnet_ids          = var.aws_route_table_ids_for_public
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.ap-northeast-1.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.aws_route_table_ids_for_public
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true
}


# s3 の vpc endpoint 作成
# resource "aws_vpc_endpoint" "s3" {
#   vpc_id            = var.vpc_id
#   service_name      = "com.amazonaws.ap-northeast-1.s3"
#   vpc_endpoint_type = "Gateway"
# }

# resource "aws_vpc_endpoint_route_table_association" "private_s3" {
#   count           = length(var.aws_route_table_ids_for_public)
#   vpc_endpoint_id = aws_vpc_endpoint.s3.id
#   route_table_id  = var.aws_route_table_ids_for_public[count.index]
# }


# # ECS から SSM にアクセスするために必要なVPCエンドポイント
# resource "aws_vpc_endpoint" "ssm" {
#   vpc_id              = var.vpc_id
#   service_name        = "com.amazonaws.ap-northeast-1.ssm"
#   vpc_endpoint_type   = "Interface"
#   subnet_ids          = var.aws_route_table_ids_for_public
#   security_group_ids  = [aws_security_group.vpc_endpoint.id]
#   private_dns_enabled = true
# }

# ECS から cloudwatch にアクセスするために必要なVPCエンドポイント
# resource "aws_vpc_endpoint" "cloudwatch" {
#   vpc_id              = var.vpc_id
#   service_name        = "com.amazonaws.ap-northeast-1.monitoring"
#   vpc_endpoint_type   = "Interface"
#   subnet_ids          = var.aws_route_table_ids_for_public
#   security_group_ids  = [aws_security_group.vpc_endpoint.id]
#   private_dns_enabled = true
# }

# ECS から cloudwatch にアクセスするために必要なVPCエンドポイント
resource "aws_vpc_endpoint" "cloudwatch_logs" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.ap-northeast-1.logs"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.aws_route_table_ids_for_public
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true
}
