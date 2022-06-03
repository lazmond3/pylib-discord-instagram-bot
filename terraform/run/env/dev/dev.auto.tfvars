app_name = "discord-instagram-bot"

# route53, cert
app_domain  = "discord-instagram-bot.moikilo00.net"
root_domain = "moikilo00.net"

# vpc
vpc_azs                  = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
vpc_public_subnet_cidrs  = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
vpc_private_subnet_cidrs = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]

ecr_name = "discord-instagram-bot"

template_file_path = "../../../module/ecs/discord_pyhton.json.tpl" # main.tf からの相対パス

container_repository = "554506578892.dkr.ecr.ap-northeast-1.amazonaws.com/discord-instagram-bot"
container_tag        = "1.1.0-4b01314"

container_name = "discord-instagram-bot" # でいいのか？
# container_name = "nginx" # でいいのか？
# これなんでもいい
# container_port = "8080" # でいいのか？
container_port = "80" # でいいのか？

task_mysql_database = "discord"
task_mysql_user     = "user"
task_db_port        = "3306"

cert_arn = "arn:aws:acm:ap-northeast-1:554506578892:certificate/de18d8c0-ab5d-43ae-b5e8-dd8143d96a4d"

cert_route53_zone_main_id = "Z04052072YGY8CIREK2A2"
