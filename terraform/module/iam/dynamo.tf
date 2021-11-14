resource "aws_dynamodb_table" "tweet_json" {
  name           = "tweet_json"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "tweet_id"


  attribute {
    name = "tweet_id"
    type = "S"
  }

  tags = {
    Name        = "tweet_json"
    Environment = "production"
  }
}


# lambda policy
resource "aws_iam_policy" "iam_dynamo_tweet_json" {
  name = "lambda_dynamo_music-policy"
  path = "/"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadWriteTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "${aws_dynamodb_table.tweet_json.arn}*"
        }
    ]
}
EOF
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "tweet_json" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.iam_dynamo_tweet_json.arn
}
