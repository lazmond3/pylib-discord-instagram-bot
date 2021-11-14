import os

import requests
from debug import DEBUG

MID = os.getenv("MID")
SESSIONID = os.getenv("SESSIONID")

# クッキーの使い方がわかるファイル
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


cookie["mid"] = MID
cookie["sessionid"] = SESSIONID

def requests_get_cookie(url, expire=1000):
    data = requests.get(url, cookies=cookie)
    return data.text
