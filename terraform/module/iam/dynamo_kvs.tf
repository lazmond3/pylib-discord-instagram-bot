resource "aws_dynamodb_table" "dynamo_kvs" {
  name           = "dynamo_kvs"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "key"


  attribute {
    name = "key"
    type = "S"
  }

  tags = {
    Name        = "dynamo_kvs"
    Environment = "production"
  }
}


# lambda policy
resource "aws_iam_policy" "iam_dynamo_dynamo_kvs" {
  name = "dynamo_kvs-policy"
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
            "Resource": "${aws_dynamodb_table.dynamo_kvs.arn}*"
        }
    ]
}
EOF
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "dynamo_kvs" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.iam_dynamo_dynamo_kvs.arn
}
