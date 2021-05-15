app_name = "discord-instagram-bot"

# route53, cert
app_domain  = "discord-instagram-bot.moikilo00.net"
root_domain = "moikilo00.net"

# vpc
vpc_azs                  = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
vpc_public_subnet_cidrs  = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
vpc_private_subnet_cidrs = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]

ecr_name = "discord-instagram-bot"

template_file_path = "../../../module/ecs/nginx_template.json" # main.tf からの相対パス

container_repository = "554506578892.dkr.ecr.ap-northeast-1.amazonaws.com/discord-instagram-bot"
container_tag        = "1.0.0-c51121e"

container_name = "discord-instagram-bot" # でいいのか？
# これなんでもいい
container_port = "8080" # でいいのか？

task_mysql_database = "discord"
task_mysql_user     = "user"
task_db_port        = "3306"

cert_arn = "arn:aws:acm:ap-northeast-1:554506578892:certificate/8c4660bc-e960-4e74-8de0-4beb26637621"

cert_route53_zone_main_id = "Z04052072YGY8CIREK2A2"
