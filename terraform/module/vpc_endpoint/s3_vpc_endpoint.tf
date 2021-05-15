# s3 の vpc endpoint 作成
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.ap-northeast-1.s3"
  vpc_endpoint_type = "Gateway"
}


resource "aws_vpc_endpoint_route_table_association" "private_s3" {
  count           = length(var.vpc_aws_route_table_id_for_private_list)
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
  route_table_id  = var.vpc_aws_route_table_id_for_private_list[count.index]
}
