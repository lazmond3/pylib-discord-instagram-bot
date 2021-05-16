resource "aws_route53_record" "main" {
  type = "A"

  name    = var.app_domain
  zone_id = var.cert_route53_zone_main_id

  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
