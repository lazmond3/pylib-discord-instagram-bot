resource "aws_dynamodb_table" "instagram_json" {
  name           = "instagram_json"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "instagram_id"


  attribute {
    name = "instagram_id"
    type = "S"
  }

  tags = {
    Name        = "instagram_json"
    Environment = "production"
  }
}


# lambda policy
resource "aws_iam_policy" "iam_dynamo_instagram_json" {
  name = "instagram_json-policy"
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
            "Resource": "${aws_dynamodb_table.instagram_json.arn}*"
        }
    ]
}
EOF
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "instagram_json" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.iam_dynamo_instagram_json.arn
}
