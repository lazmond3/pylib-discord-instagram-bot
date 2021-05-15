[
  {
    "name": "${container_name}",
    "image": "${container_repository}:${container_tag}",
    "secrets": [
      {
        "name": "TOKEN",
        "valueFrom": "${token}"
      },
      {
        "name": "CONSUMER_KEY",
        "valueFrom": "${consumer_key}"
      },
      {
        "name": "CONSUMER_SECRET",
        "valueFrom": "${consumer_secret}"
      },
      {
        "name": "MID",
        "valueFrom": "${mid}"
      },
      {
        "name": "SESSIONID",
        "valueFrom": "${mid}"
      }
    ]
    "environment": [
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
