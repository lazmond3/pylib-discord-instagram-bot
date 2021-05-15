variable "app_domain" {
  type = string
}

# cert から (route53 の本体)
variable "cert_route53_zone_main_id" {
  type = string
}

# alb から
variable "alb_dns_name" {
  type = string
}
variable "alb_zone_id" {
  type = string
}
