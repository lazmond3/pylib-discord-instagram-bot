[
  {
    "name": "${container_name}",
    "image": "554506578892.dkr.ecr.ap-northeast-1.amazonaws.com/sample-python2:latest",
    "portMappings": [
      {
        "containerPort": 8080,
        "hostPort": 8080
      }
    ],
    "secrets": [
      {
        "name": "PASS",
        "valueFrom": "${database_password}"
      }
    ],
    "environment": [
      {
        "name": "DB_DATABASE",
        "value": "${mysql_database}"
      },
      {
        "name": "USER",
        "value": "${mysql_user}"
      },
      {
        "name": "ENDPOINT",
        "value": "${db_address}"
      },
      {
        "name": "PORT",
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
