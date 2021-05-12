resource "aws_api_gateway_rest_api" "discord_endpoint" {
  name        = "discord_endpoint"
  description = "Discord の hookイベントをこのエンドポイントに入力したい"
}

# ref: https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.discord_endpoint.id
  parent_id   = aws_api_gateway_rest_api.discord_endpoint.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.discord_endpoint.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.discord_endpoint.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_function.invoke_arn
}
