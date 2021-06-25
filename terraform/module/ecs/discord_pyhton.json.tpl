[
  {
    "name": "${container_name}",
    "image": "${container_repository}:${container_tag}",
    "secrets": [
      {
        "name": "TOKEN",
        "valueFrom": "${token_arn}"
      },
      {
        "name": "CONSUMER_KEY",
        "valueFrom": "${consumer_key_arn}"
      },
      {
        "name": "CONSUMER_SECRET",
        "valueFrom": "${consumer_secret_arn}"
      },
      {
        "name": "MID",
        "valueFrom": "${mid_arn}"
      },
      {
        "name": "SESSIONID",
        "valueFrom": "${sessionid_arn}"
      },
      {
        "name": "AWS_ACCESS_KEY_ID",
        "valueFrom": "${aws_access_key_id_arn}"
      },
      {
        "name": "AWS_SECRET_ACCESS_KEY",
        "valueFrom": "${aws_secret_access_key_arn}"
      }
    ],
    "environment": [
      {
        "name": "CONTAINER_TAG",
        "value": "${container_tag}"
      },
      {
        "name": "DEBUG",
        "value": "1"
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
