import json
import os
from logging import DEBUG, INFO, LogRecord, StreamHandler, getLogger
from typing import Any, Dict, List, Optional, cast

import requests

from ...boto3 import add_json_to_dynamo_tweet_json
from ...const_value import IS_DEBUG, TW_CONSUMER_KEY, TW_CONSUMER_SECRET
from .base64_util import base64_encode_str
from .twitter_image import TwitterImage, convert_twitter

logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def mkdir_notexists(dirs: List[str]):
    for dirpath in dirs:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            logger.info(f"[mkdir_noexists] mkdir {dirpath}")


if not IS_DEBUG:
    logger.setLevel(INFO)


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
    # TODO: もし正常に保存できてたら、という条件ができれば
    # if os.path.exists(f"dump_json/dump_one_{tweet_id}.json"):
    #     with open(f"dump_json/dump_one_{tweet_id}.json", 'r') as f:
    #         js = json.load(f)

    #     # print(f"js: {js}")
    #     # TODO: logger を利用して出す
    #     tw = convert_twitter(js)
    #     logger.debug(
    #         f"[cached] video: {tw.video_url} images: {' '.join(tw.image_urls)}")
    #     return tw

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

    print(f"js: {js}")
    tw = convert_twitter(js)
    logger.debug(f"video: {tw.video_url} images: {','.join(tw.image_urls)}, ")
    return tw


def get_tweets_of_user(
    screen_name: str,
    since_id: Optional[str] = None,  # 最小の、この要素を含めないid。これより新しいツイートが検索される
    max_id: Optional[str] = None,  # これを含めるかこれ以下の
    is_second: bool = False,
):
    logger.debug(f"[get_tweets_of_user] screen_name: {screen_name}")
    if not os.path.exists(TOKEN_FILENAME):
        get_auth_wrapper()
    with open(TOKEN_FILENAME) as f:
        s = json.load(f)
        token = s["access_token"]

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {"screen_name": screen_name, "tweet_mode": "extended"}

    if since_id:
        params["since_id"] = since_id  # nopep8
    if max_id:
        params["max_id"] = max_id  # nopep8

    headers = {"Authorization": f"Bearer {token}"}

    # キャッシュを利用する.
    mkdir_notexists([f"dump_tweet_of_user"])
    fname = f"dump_tweet_of_user/dump_user_{screen_name}.json"
    if os.path.exists(fname):
        with open(fname, "r") as f:
            js = json.load(f)
        # tw = convert_twitter(js)
        return

    # r = requests.get(url, params=params, headers=headers)
    r = None
    try:
        r = requests.get(url, params=params, headers=headers)
    except Exception:
        print(f"error exception?? : {r.status_code}")
        if not is_second:
            os.remove(TOKEN_FILENAME)
            get_auth_wrapper()
            # もう一度実行する
            get_tweets_of_user(screen_name, since_id, max_id, True)

    tx = r.text
    print(f"tx: {tx}")
    js = text_to_dict(tx)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False)
    # 直し方がよくわからないので、json の結果を利用させてもらう。
    # with open(fname) as f:
    # txt_decoded = f.read()

    # tw = convert_twitter(js)
    # logger.debug(f"video: {tw.video_url} images: {','.join(tw.image_urls)}, ")
    # return tw


def get_following_list(screen_name: str, cursor: int = -1, count: int = 200):
    logger.debug(f"[get_following_list] screen_name: {screen_name}")
    if not os.path.exists(TOKEN_FILENAME):
        get_auth_wrapper()
    with open(TOKEN_FILENAME) as f:
        s = json.load(f)
        token = s["access_token"]

    url = "https://api.twitter.com/1.1/friends/list.json"
    params = {"screen_name": screen_name, "cursor": cursor, "count": count}

    headers = {"Authorization": f"Bearer {token}"}

    # キャッシュを利用する.
    mkdir_notexists([f"dump_following"])
    fname = f"dump_following/following_{screen_name}_{cursor}.json"
    if os.path.exists(fname):
        with open(fname, "r") as f:
            js = json.load(f)
        return

    r = None
    try:
        r = requests.get(url, params=params, headers=headers)
    except Exception:
        print(f"error exception?? : failed to fetch")
        return

    tx = r.text
    print(f"tx: {tx}")
    js = text_to_dict(tx)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False)


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

    # TODO: ダウンロードはできるけど、どうしたものか。
    if js["in_reply_to_status_id_str"]:
        get_sumatome(js["in_reply_to_status_id_str"])

    # キャッシュを利用する.
    # with open(f"dump_one_{tweet_id}.json", 'r') as f:
    #     js = json.load(f)


if __name__ == "__main__":
    # get_oauth1()
    # get_auth_wrapper()

    # get_one_tweet("1372519422380797955")
    # https://twitter.com/Malong777888/status/1409827218948165632
    # tw = get_one_tweet("1409827218948165632") # video
    import sys

    tw = get_one_tweet(sys.argv[1])  # video
    print(tw)
    # get_one_tweet("1373208627356442626")
    # with open("dump_one.json") as f:
    #     js = json.load(f)
    # image = convert_twitter(js)
    # print(image)
