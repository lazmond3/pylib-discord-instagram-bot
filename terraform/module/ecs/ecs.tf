# ECS は、
# - cluster, 
# - task_definition (コンテナの定義, ポートの定義, data plane の定義:FARGATE)
# - service 
# から構成される
resource "aws_ecs_cluster" "main" {
  name = var.app_name
}

# Task Definition
# https://www.terraform.io/docs/providers/aws/r/ecs_task_definition.html
resource "aws_ecs_task_definition" "main" {
  family = "${var.app_name}-task-definition"

  # データプレーンの選択
  requires_compatibilities = ["FARGATE"]

  # ECSタスクが使用可能なリソースの上限
  # タスク内のコンテナはこの上限内に使用するリソースを収める必要があり、メモリが上限に達した場合OOM Killer にタスクがキルされる
  cpu    = "256"
  memory = "512"

  # ECSタスクのネットワークドライバ
  # Fargateを使用する場合は"awsvpc"決め打ち
  network_mode = "awsvpc"

  # ECR にアクセスするための IAM Role
  execution_role_arn = var.ecs_task_execution_role_arn

  # 起動するコンテナの定義
  # 「nginxを起動し、80ポートを開放する」設定を記述。
  container_definitions = data.template_file.container_definitions.rendered
}


####################
# ecs-service
####################

# ECS Service
# https://www.terraform.io/docs/providers/aws/r/ecs_service.html
resource "aws_ecs_service" "main" {
  name = var.app_name

  # 依存関係の記述。
  # "aws_lb_listener_rule.main" リソースの作成が完了するのを待ってから当該リソースの作成を開始する。
  # "depends_on" は "aws_ecs_service" リソース専用のプロパティではなく、Terraformのシンタックスのため他の"resource"でも使用可能
  # depends_on = var.aws_ecs_services_depends_on

  # 当該ECSサービスを配置するECSクラスターの指定
  cluster = aws_ecs_cluster.main.name

  # データプレーンとしてFargateを使用する
  launch_type = "FARGATE"

  # ECSタスクの起動数を定義
  desired_count = var.ecs_desired_count

  # 起動するECSタスクのタスク定義
  task_definition = aws_ecs_task_definition.main.arn

  # ECSタスクへ設定するネットワークの設定
  network_configuration {
    # タスクの起動を許可するサブネット
    subnets = var.ecs_subnets
    # タスクに紐付けるセキュリティグループ
    security_groups = [var.aws_security_group_ecs_id]
  }

  # ECSタスクの起動後に紐付けるELBターゲットグループ
  load_balancer {
    target_group_arn = var.ecs_load_balancer_target_arn
    container_name   = var.container_name # var.app_name にしたい
    container_port   = var.container_port # 8080
  }

}
