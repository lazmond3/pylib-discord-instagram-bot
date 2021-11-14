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
dynamo = boto3.resource('dynamodb', region_name='ap-northeast-1')
tweet_json = dynamo.Table("tweet_json")
instagram_json = dynamo.Table("instagram_json")

s3 = boto3.resource("s3")
bucket = s3.Bucket("discord-python-video")
bucket_image = s3.Bucket("discord-python-image")


def add_json_to_tweet_json(tweet_id: str, data: str):
    tweet_json.put_item(
        Item={
            'tweet_id': tweet_id,
            'data': data
        }
    )
def add_instagram_json_to_instagram_json(instagram_url: str, instagram_id: str, data: str):
    """
    sample url: https://www.instagram.com/p/CVNB-GNldga/
    """
    
    instagram_json.put_item(
        Item={
            'instagram_id': instagram_id,
            'data': data
        }
    )


def upload_video_file(fname: str) -> str:
    bucket.upload_file(fname, fname, ExtraArgs={'ContentType': "video/mp4"})
    basename = os.path.basename(fname)
    return f"https://discord-python-video.s3.ap-northeast-1.amazonaws.com/{basename}"


def upload_image_file(fname: str, tweet_num: str, index: int):
    # 1つめ: ファイルパス 2: object key
    # https://dev.classmethod.jp/articles/boto3-s3-object-put-get/
    ext = fname.split(".")[1]
    content_type = ""
    if ext == "jpg" or ext == "jpeg":
        content_type = "image/jpeg"
    elif ext == "png":
        content_type = "image/png"
    bucket_image.upload_file(fname, f"{tweet_num}/{index}.{ext}", ExtraArgs={'ContentType': content_type})
    basename = os.path.basename(fname)

    return f"https://discord-python-image.s3.ap-northeast-1.amazonaws.com/{tweet_num}/{index}.{ext}"


if __name__ == "__main__":
    # fname = "1408027129644605440.mp4"
    # bucket.upload_file(fname, fname)

    # 読み込み
    data = tweet_json.get_item(Key={
        'tweet_id': "1459491452048740352"
    })
    print(f"data: {data} type: {type(data['Item'])}")
    print(f"data: {data['Item']['data']} type: {type(data['Item']['data'])}")

    import json
    js = json.loads(data['Item']['data'])
    print(f"js: {js}")

    # 書き込み
    # with open("dump_one_1459491452048740352.json") as f:
    #     ustr = f.read()
    #     # add_json_to_tweet_json("1459491452048740352", ustr)
