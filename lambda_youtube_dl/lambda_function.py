import os
import json
import requests
import boto3
import youtube_dl

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
s3 = boto3.resource("s3")
bucket = s3.Bucket("discord-python-video")


def upload_video_file(fname: str) -> str:
    """
    fname はファイルのある位置。object key は basenameを利用する。
    """
    base_fname = os.path.basename(fname)
    # 第二引数はkey
    bucket.upload_file(fname, base_fname, ExtraArgs={"ContentType": "video/mp4"})
    basename = os.path.basename(fname)
    return f"https://discord-python-video.s3.ap-northeast-1.amazonaws.com/{basename}"


def lambda_handler(event, context):
    res = requests.get("http://www.yahoo.co.jp/")

    webhook_url = event["url"]
    ydlmp4 = youtube_dl.YoutubeDL(
        {
            "outtmpl": "/tmp/%(id)s" + ".mp4",
            "format": "18",
        }
    )
    info_dict = ydlmp4.extract_info(webhook_url, download=True)
    id_name = info_dict["id"]
    old_fname = "/tmp/" + id_name + ".mp4"
    replaced_title = (
        info_dict["title"]
        .replace(" ", "_")
        .replace("　", "__")
        .replace('"', "'")
        .replace("/", "__")
    )
    fname = "/tmp/" + id_name + "-" + replaced_title + ".mp4"
    if os.path.exists(old_fname):
        assert os.path.exists(old_fname)
        os.rename(old_fname, fname)

    uploaded_url = upload_video_file(fname)


    headers = {'content-type': 'application/json'}
    payload = {'content': f'[youtube-dl finished] {info_dict["title"]} {uploaded_url}'}

    requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

    return {
        'statusCode': 200,
        'myStatusCode': res.status_code,
        'body': json.dumps('Hello from Lambda!')
    }
