variable "vpc_id" {
  type = string
}
variable "vpc_cidr" {
  type = string
}
variable "vpc_aws_subnet_private_ids" {
  type = list(string)
}

variable "vpc_aws_route_table_id_for_private_list" {
  type = list(string)
}
