output "vpc_id" {
  value = aws_vpc.main.id
}
output "vpc_aws_subnet_public_ids" {
  value = aws_subnet.publics.*.id
}
output "vpc_aws_subnet_private_ids" {
  value = aws_subnet.privates.*.id
}

output "vpc_aws_route_table_id_for_public" {
  value = aws_route_table.public.id
}
output "vpc_aws_route_table_id_for_private_list" {
  value = aws_route_table.privates.*.id
}
