# arn:aws:acm:ap-northeast-1:554506578892:certificate/8c4660bc-e960-4e74-8de0-4beb26637621
output "cert_arn" {
  value = aws_acm_certificate.main.arn
}

# Z04052072YGY8CIREK2A2
output "cert_route53_zone_main_id" {
  # value = cert.cert_route53_zone_main_id
  value = data.aws_route53_zone.main.id
}
