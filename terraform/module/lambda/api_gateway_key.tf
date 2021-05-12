# resource "aws_api_gateway_api_key" "example" {
#   name    = "example_api_key"
#   enabled = true
# }

# resource "aws_api_gateway_usage_plan" "example" {
#   name       = "example_usage_plan"
#   depends_on = [aws_api_gateway_deployment.example]

#   api_stages {
#     api_id = aws_api_gateway_rest_api.discord_endpoint.id
#     stage  = aws_api_gateway_deployment.example.stage_name
#   }
# }

# resource "aws_api_gateway_usage_plan_key" "example" {
#   key_id        = aws_api_gateway_api_key.example.id
#   key_type      = "API_KEY"
#   usage_plan_id = aws_api_gateway_usage_plan.example.id
# }
