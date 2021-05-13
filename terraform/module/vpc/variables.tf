variable "app_name" {}

variable "azs" {
  type    = list(string)
  default = ["ap-northeast-1a", "ap-northeast-1c"]
#   default = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
#   default = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
  default = ["10.0.0.0/24"]
}
