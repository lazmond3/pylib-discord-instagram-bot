from logging import LogRecord, getLogger,StreamHandler,DEBUG,INFO
logger = getLogger(__name__)    #以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

import json
import os
from typing import Any, Dict, Optional, cast

import requests
from ...const_value import IS_DEBUG

if not IS_DEBUG:
    logger.setLevel(INFO)

from .base64_util import base64_encode_str
from .twitter_image import TwitterImage, convert_twitter
from ...boto3 import add_json_to_dynamo_tweet_json

from ...const_value import TW_CONSUMER_KEY, TW_CONSUMER_SECRET

# const
TOKEN_FILENAME: str = ".token.json"


def _make_basic(consumer_key: str, consumer_secret: str) -> str:
    concat = f"{consumer_key}:{consumer_secret}"
    converted = base64_encode_str(concat)
    return cast(str, converted)


def _get_auth(url: str, basic: str) -> None:
    """
    twitter API の access token を取得する __inner__
    """
    headers = {"Authorization": f"Basic {basic}"}
    payload = {"grant_type": "client_credentials"}
    r = requests.post(url, headers=headers, params=payload)

    if IS_DEBUG:
        logger.debug(r)
        logger.debug("-------")
        logger.debug(r.text)
    with open(TOKEN_FILENAME, "w") as f:
        f.write(r.text)


def get_auth_wrapper() -> None:
    """
    twitter API の access token を取得する __wrapper__
    """
    if not all([TW_CONSUMER_KEY, TW_CONSUMER_SECRET]):
        print("specify consumer key/secret")
        exit(1)
    assert TW_CONSUMER_KEY
    assert TW_CONSUMER_SECRET

    basic = cast(str, _make_basic(TW_CONSUMER_KEY, TW_CONSUMER_SECRET))
    url = "https://api.twitter.com/oauth2/token"
    _get_auth(url, basic)


# テスト
def text_to_dict(str_: str) -> Dict[str, Any]:
    js = json.loads(str_)
    return cast(Dict[str, Any], js)

def get_one_tweet(tweet_id: str, is_second: bool = False) -> TwitterImage:
    logger.debug(f"[get_one_tweet] tweet_id: {tweet_id}")
    if not os.path.exists(TOKEN_FILENAME):
        get_auth_wrapper()
    with open(TOKEN_FILENAME) as f:
        s = json.load(f)
        token = s["access_token"]

    url = "https://api.twitter.com/1.1/statuses/show.json"
    params = {"id": tweet_id, "tweet_mode": "extended"}
    headers = {"Authorization": f"Bearer {token}"}

    # キャッシュを利用する.
    if os.path.exists(f"dump_json/dump_one_{tweet_id}.json"):
        with open(f"dump_json/dump_one_{tweet_id}.json", 'r') as f:
            js = json.load(f)
        tw = convert_twitter(js)
        logger.debug(f"[cached] video: {tw.video_url} images: {' '.join(tw.image_urls)}")
        return tw

    try:
        r = requests.get(url, params=params, headers=headers)
    except Exception:
        if not is_second:
            os.remove(TOKEN_FILENAME)
            get_auth_wrapper()
            # もう一度実行する
            get_one_tweet(tweet_id, True)

    tx = r.text
    js = text_to_dict(tx)

    with open(f"dump_json/dump_one_{tweet_id}.json", "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False)
    # 直し方がよくわからないので、json の結果を利用させてもらう。
    with open(f"dump_json/dump_one_{tweet_id}.json") as f:
        txt_decoded = f.read()
        add_json_to_dynamo_tweet_json(tweet_id, txt_decoded)

    tw = convert_twitter(js)
    logger.debug(f"video: {tw.video_url} images: {','.join(tw.image_urls)}, ")
    return tw


def get_sumatome(tweet_id: str, is_second: bool = False) -> None:
    if not os.path.exists(TOKEN_FILENAME):
        get_auth_wrapper()
    with open(TOKEN_FILENAME) as f:
        s = json.load(f)
        token = s["access_token"]

    url = "https://api.twitter.com/1.1/statuses/show.json"
    params = {"id": tweet_id}
    headers = {"Authorization": f"Bearer {token}"}

    try:
        r = requests.get(url, params=params, headers=headers)
    except Exception:
        if not is_second:
            os.remove(TOKEN_FILENAME)
            get_auth_wrapper()
            # もう一度実行する
            get_one_tweet(tweet_id, True)

    tx = r.text
    js = text_to_dict(tx)

    # デバッグのためのダンプ
    with open(f"dump_one_{tweet_id}.json", "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False)
    # 直し方がよくわからないので、json の結果を利用させてもらう。
    with open(f"dump_one_{tweet_id}.json") as f:
        txt_decoded = f.read()
        add_json_to_dynamo_tweet_json(tweet_id, txt_decoded)


    if not js["in_reply_to_status_id_str"]:
        get_one_tweet(js["in_reply_to_status_id_str"])

    # キャッシュを利用する.
    # with open(f"dump_one_{tweet_id}.json", 'r') as f:
    #     js = json.load(f)


if __name__ == "__main__":
    # get_oauth1()
    # get_auth_wrapper()

    # get_one_tweet("1372519422380797955")
    # https://twitter.com/Malong777888/status/1409827218948165632
    # tw = get_one_tweet("1409827218948165632") # video
    tw = get_one_tweet("1407925711277486082")  # video
    print(tw)
    # get_one_tweet("1373208627356442626")
    # with open("dump_one.json") as f:
    #     js = json.load(f)
    # image = convert_twitter(js)
    # print(image)
