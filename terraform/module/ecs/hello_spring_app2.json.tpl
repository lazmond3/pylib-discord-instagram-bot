[
  {
    "name": "${container_name}",
    "image": "554506578892.dkr.ecr.ap-northeast-1.amazonaws.com/line-bot-sample2-app2:0.0.1-44327f5",
    "portMappings": [
      {
        "containerPort": 8080,
        "hostPort": 8080
      }
    ],
    "secrets": [
      {
        "name": "DB_PASSWORD",
        "valueFrom": "${database_password}"
      }
    ],
    "environment": [
      {
        "name": "DB_DATABASE",
        "value": "${mysql_database}"
      },
      {
        "name": "DB_USER",
        "value": "${mysql_user}"
      },
      {
        "name": "DB_ADDRESS",
        "value": "${db_address}"
      },
      {
        "name": "DB_PORT",
        "value":  "${db_port}"
      },
      {
        "name": "CONTAINER_TAG",
        "value":  "${container_tag}"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "ap-northeast-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }
]
