from .const_value import IS_DEBUG, INSTA_MID, INSTA_SESSIONID
import requests
from logging import getLogger, StreamHandler, INFO

logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


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
            if IS_DEBUG:
                logger.debug("split: ", each.split("="))
            key, v = each.split("=")[0], "".join(each.split("=")[1:])
            cookie2[key] = v
    for k in cookie2.keys():
        if k in ["mid", "sessionid"]:
            cookie[k] = cookie2[k]
    return cookie


cookie["mid"] = INSTA_MID
cookie["sessionid"] = INSTA_SESSIONID


def requests_get_cookie(url, expire=1000):
    data = requests.get(url, cookies=cookie)
    return data.text
