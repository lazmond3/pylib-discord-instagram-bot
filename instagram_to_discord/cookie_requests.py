import requests
import json
from debug import DEBUG
from .redis_cli import store_data, get_data

# クッキーの使い方がわかるファイル

# cookie2.txt をこのように使うと、クッキーを使ったリクエストができるっぽい！
# DANGER instagram の cookie が別サイトにも送信されてしまいうる。
cookie = dict()


def make_cookie(path):
    global cookie
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
            cookie[key] = v
    return cookie


make_cookie("cookie2.txt")

# redis 機能を加える


def requests_get_cookie(url, expire=1000):
    cache = get_data(url)
    if cache:
        return cache
    else:
        data = requests.get(url, cookies=cookie)
        store_data(url, data.text, expire)
        return data.text
