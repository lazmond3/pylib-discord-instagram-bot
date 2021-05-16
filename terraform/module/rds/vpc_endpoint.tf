resource "aws_vpc_endpoint" "rds" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.ap-northeast-1.rds"
  vpc_endpoint_type = "Interface"
  #The ID of one or more subnets in which to create a network interface for the endpoint.
  # その中にネットワークインターフェース(VPCエンドポイント)を作るためのサブネットのID
  # プライベートサブネットに外部ヘ行く道がなくて困っているので、VPCエンドポイントを作成する？
  #Applicable for endpoints of type GatewayLoadBalancer and Interface.

  subnet_ids          = var.aws_lb_private_ids
  security_group_ids  = [aws_security_group.vpc_endpoint_rds.id, aws_security_group.vpc_endpoint_rds2.id]
  private_dns_enabled = true
}
