# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster#endpoint
output "db_address" {
  value = aws_rds_cluster.this.endpoint
}
output "db_port" {
  value = aws_rds_cluster.this.port
}
