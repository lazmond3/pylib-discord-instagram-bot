import aws_lambda_typing as lambda_typing

def handler(event: lambda_typing.SQSEvent, context: lambda_typing.Context) -> None:
    for record in event['Records']:
        print(context.get_remaining_time_in_millis())
        print(record['body'])
