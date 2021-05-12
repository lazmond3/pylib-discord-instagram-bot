terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_s3_bucket" "discord-python-bot-lambda" {
  bucket = "discord-python-bot-lambda"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "discord-python-bot-lambda/tfstate"
    Environment = "Dev"
  }
}
