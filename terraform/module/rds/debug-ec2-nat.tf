# # NAT ゲートウェイ 用 Elastic IP付与 (public に NAT ゲートウェイを接続)
# resource "aws_eip" "nat" {
#   vpc = true

#   tags = {
#     Name = "ec2-private-debug-natgw-0"
#   }
# }

# # # NAT ゲートウェイ
# resource "aws_nat_gateway" "this" {
#   #   count = length(var.public_subnet_cidrs)

#   subnet_id     = var.aws_lb_public_ids[0]
#   allocation_id = aws_eip.nat.id # ここで eip をつないでいる

#   tags = {
#     Name = "line-bot-nat-gateway-diff"
#   }
# }

# # NATをオフにする
# resource "aws_route" "privates" {
#   destination_cidr_block = "0.0.0.0/0"

#   route_table_id = var.debug_ec2_aws_route_table_id_0
#   nat_gateway_id = aws_nat_gateway.this.id
# }
