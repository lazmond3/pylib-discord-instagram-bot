import requests
import json

# クッキーの使い方がわかるファイル

# cookie2.txt をこのように使うと、クッキーを使ったリクエストができるっぽい！
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
def requests_get_cookie(url):
    return requests.get(url, cookies=cookie)
