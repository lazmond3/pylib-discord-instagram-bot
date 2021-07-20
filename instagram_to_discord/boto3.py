import os

import boto3
from botocore.config import Config

proxy_definitions = {
    "http": "http://proxy.amazon.com:6502",
    "https": "https://proxy.amazon.org:2010",
}

my_config = Config(
    region_name="ap-northeast-1",
    signature_version="v4"
    # proxies=proxy_definitions
)

# boto3_client = boto3.client('kinesis', config=my_config)
boto3_s3 = boto3.client("s3", config=my_config)

s3 = boto3.resource("s3")
bucket = s3.Bucket("discord-python-video")


# returns file URL
def upload_file(fname: str) -> str:
    bucket.upload_file(fname, fname)
    basename = os.path.basename(fname)
    return f"https://discord-python-video.s3.ap-northeast-1.amazonaws.com/{basename}"


if __name__ == "__main__":
    fname = "1408027129644605440.mp4"
    # with open(fname, 'rb')  as fb:
    #     boto3_s3.upload_fileobj(fb, "discord-python-video",  fname)
    # with open(fname, 'rb')  as fb:
    bucket.upload_file(fname, fname)
