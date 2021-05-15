# NAT ゲートウェイ 用 Elastic IP付与 (public に NAT ゲートウェイを接続)
# resource "aws_eip" "nat" {
#   count = length(var.public_subnet_cidrs)

#   vpc = true

#   tags = {
#     Name = "${var.app_name}-natgw-${count.index}"
#   }
# }

# # NAT ゲートウェイ
# resource "aws_nat_gateway" "this" {
#   count = length(var.public_subnet_cidrs)

#   subnet_id     = element(aws_subnet.publics.*.id, count.index)
#   allocation_id = element(aws_eip.nat.*.id, count.index) # ここで eip をつないでいる

#   tags = {
#     Name = "${var.app_name}-${count.index}"
#   }
# }

# NATをオフにする
# resource "aws_route" "privates" {
#   count = length(var.private_subnet_cidrs)

#   destination_cidr_block = "0.0.0.0/0"

#   route_table_id = element(aws_route_table.privates.*.id, count.index)
#   nat_gateway_id = element(aws_nat_gateway.this.*.id, count.index)
# }
