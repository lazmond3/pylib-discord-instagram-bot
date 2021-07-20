import os
import requests
from debug import DEBUG

from .redis_cli import REDIS_PASS


MID = os.getenv("MID")
SESSIONID = os.getenv("SESSIONID")

if REDIS_PASS:
    from .redis_cli import get_data, store_data

# クッキーの使い方がわかるファイル
# DANGER instagram の cookie が別サイトにも送信されてしまいうる。
cookie = dict()


def make_cookie(path):
    global cookie
    cookie2 = dict()
    with open(path) as f:
        alltext = []
        for line in f.readlines():
            alltext.append(line.strip())
        text = "".join(alltext)
        splited = text.split("; ")
        for each in splited:
            if DEBUG:
                print("split: ", each.split("="))
            key, v = each.split("=")[0], "".join(each.split("=")[1:])
            cookie2[key] = v
    for k in cookie2.keys():
        if k in ["mid", "sessionid"]:
            cookie[k] = cookie2[k]
    return cookie


# if COOKIE_PATH:
#     make_cookie(COOKIE_PATH)
# else:
cookie["mid"] = MID
cookie["sessionid"] = SESSIONID

# redis 機能を加える

if REDIS_PASS:
    # 本当は導通確認でもいいかも。
    def requests_get_cookie(url, expire=1000):
        cache = get_data(url)
        if cache:
            return cache
        else:
            data = requests.get(url, cookies=cookie)
            store_data(url, data.text, expire)
            return data.text


else:

    def requests_get_cookie(url, expire=1000):
        data = requests.get(url, cookies=cookie)
        return data.text
