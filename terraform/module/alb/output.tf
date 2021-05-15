output "alb_dns_name" {
  value = aws_lb.this.dns_name
}
output "alb_zone_id" {
  value = aws_lb.this.zone_id
}
output "alb_listener_rule_resource" {
  value = aws_lb_listener_rule.main
}
output "alb_target_group_main_arn" {
  value = aws_lb_target_group.main.arn
}
