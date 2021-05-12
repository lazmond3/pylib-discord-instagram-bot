import aws_lambda_typing as lambda_typing

def handler(event: lambda_typing.APIGatewayProxyEventV1, context: lambda_typing.Context) -> lambda_typing.APIGatewayProxyResponseV1:
    print("event: ", event)
    return lambda_typing.APIGatewayProxyResponseV1({
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': '{"message": "Hello from AWS Lambda"}'
    })
