data "aws_route53_zone" "main" {
  name         = var.root_domain
  private_zone = false
}

# ACM
# https://www.terraform.io/docs/providers/aws/r/acm_certificate.html
# cloudfront で使いたい場合は、 us- に設定する。
resource "aws_acm_certificate" "main" {
  domain_name = var.app_domain

  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Route53 record
# https://www.terraform.io/docs/providers/aws/r/route53_record.html
resource "aws_route53_record" "validations" {
  depends_on = [aws_acm_certificate.main]

  zone_id = data.aws_route53_zone.main.id

  ttl = 60

  # aws provider 3.0 から set になったので for_each
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      record = dvo.resource_record_value
    }
  }

  name    = each.value.name
  records = [each.value.record]
  type    = each.value.type
}

# ACM Validate
# https://www.terraform.io/docs/providers/aws/r/acm_certificate_validation.html
resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.validations : record.fqdn]
}

# ロードバランサの名前を route53に登録するものだが、今回はとりあえずスキップ
# resource "aws_route53_record" "main" {
#   type = "A"

#   name    = var.app_domain
#   zone_id = data.aws_route53_zone.main.id

#   alias {
#     name                   = var.aws_lb_dns_name
#     zone_id                = var.aws_lb_zone_id
#     evaluate_target_health = true
#   }
# }
