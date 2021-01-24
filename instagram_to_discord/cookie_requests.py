import requests
import json
from .redis_cli import store_data, get_data

# クッキーの使い方がわかるファイル

# cookie2.txt をこのように使うと、クッキーを使ったリクエストができるっぽい！
# DANGER instagram の cookie が別サイトにも送信されてしまいうる。
cookie = dict()
with open("cookie2.txt") as f:
    alltext = []
    for line in f.readlines():
        alltext.append(line.strip())
    text = "".join(alltext)
    splited = text.split("; ")
    for each in splited:
        print("split: ", each.split("="))
        key, v = each.split("=")[0], "".join(each.split("=")[1:])
        cookie[key] = v


# redis 機能を加える
def requests_get_cookie(url, expire=1000):
    cache = get_data(url)
    if cache:
        return cache
    else:
        data = requests.get(url, cookies=cookie)
        store_data(url, data.text, expire)
        return data.text
