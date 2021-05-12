resource "aws_api_gateway_rest_api" "discord_endpoint" {
  name        = "discord_endpoint"
  description = "Discord の hookイベントをこのエンドポイントに入力したい"
}

# ref: https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway
# ref: https://tech.toreta.in/entry/2020/12/06/000000

resource "aws_api_gateway_resource" "hello_world" {
  rest_api_id = aws_api_gateway_rest_api.discord_endpoint.id
  parent_id   = aws_api_gateway_rest_api.discord_endpoint.root_resource_id
  path_part   = "hello_world"
}

resource "aws_api_gateway_method" "hello_world" {
  rest_api_id      = aws_api_gateway_rest_api.discord_endpoint.id
  resource_id      = aws_api_gateway_resource.hello_world.id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "hello_world" {
  rest_api_id = aws_api_gateway_rest_api.discord_endpoint.id
  resource_id = aws_api_gateway_resource.hello_world.id
  http_method = aws_api_gateway_method.hello_world.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  depends_on = [aws_api_gateway_method.hello_world]
}

resource "aws_api_gateway_integration" "hello_world" {
  rest_api_id             = aws_api_gateway_rest_api.discord_endpoint.id
  resource_id             = aws_api_gateway_resource.hello_world.id
  http_method             = aws_api_gateway_method.hello_world.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_function.invoke_arn
}

resource "aws_api_gateway_deployment" "example" {
  rest_api_id       = aws_api_gateway_rest_api.discord_endpoint.id
  stage_name        = "example"
  stage_description = "timestamp = ${timestamp()}"

  depends_on = [
    aws_api_gateway_integration.hello_world
  ]

  lifecycle {
    create_before_destroy = true
  }
}

# resource "aws_api_gateway_method_settings" "example" {
#   rest_api_id = aws_api_gateway_rest_api.discord_endpoint.id
#   stage_name  = aws_api_gateway_deployment.example.stage_name
#   method_path = "*/*"

#   settings {
#     data_trace_enabled = true
#     logging_level      = "INFO"
#   }
# }

# 6. API GatewayにLambda関数へのアクセスを許可
resource "aws_lambda_permission" "hello_world" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.discord_endpoint.execution_arn}/*/*"
}

output "base_url" {
  value = aws_api_gateway_deployment.example.invoke_url
}
