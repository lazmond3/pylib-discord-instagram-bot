output "vpc_id" {
  value = aws_vpc.main.id
}
output "aws_subnet_public_ids" {
  value = aws_subnet.publics.*.id
}

output "vpc_cidr" {
  value = var.vpc_cidr
}
output "aws_route_table_ids_for_public" {
  value = aws_route_table.publics.*.id
}
