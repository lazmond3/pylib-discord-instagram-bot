variable "app_domain" {
  description = "これから取得したいドメイン名"
  type        = string
  default     = "discord-bot-lambda-python.moikilo00.net"
}
variable "root_domain" {
  description = "Route 53 で管理しているルートドメイン名 (wildcard)"
  type        = string
  default     = "moikilo00.net"
}
