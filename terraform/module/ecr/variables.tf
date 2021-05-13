variable "ecr-name" {
  type = string
}
variable "vpc_id" {
  type = string
}
variable "aws_route_table_ids_for_public" {
  type = list(string)
}
variable "vpc_cidr" {
  type = string
}
