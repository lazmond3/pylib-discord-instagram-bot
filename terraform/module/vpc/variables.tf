variable "app_name" {} # line-bot-sample

variable "vpc_azs" {
  type = list(string)
}

variable "vpc_cidr" {
  type = string
}

variable "vpc_public_subnet_cidrs" {
  type = list(string)
}

variable "vpc_private_subnet_cidrs" {
  type = list(string)
}
