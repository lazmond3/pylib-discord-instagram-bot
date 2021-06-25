import boto3
from botocore.config import Config

proxy_definitions = {
    'http': 'http://proxy.amazon.com:6502',
    'https': 'https://proxy.amazon.org:2010'
}

my_config = Config(
    region_name='ap-northeast-1',
    signature_version='v4'
    # proxies=proxy_definitions
)

# boto3_client = boto3.client('kinesis', config=my_config)
boto3_s3 = boto3.resource('s3', config = my_config)
