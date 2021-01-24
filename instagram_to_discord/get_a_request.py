import requests
from redis_cli import store_data, get_data
import json
from debug import DEBUG, UPDATE


cookie = dict()
with open("cookie2.txt") as f:
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

# この関数: return dictionary


def get_json_from_url(url):
    key_name = "json_"+url
    if DEBUG:
        print("key_name: ", key_name)
    text = ""
    if UPDATE:
        data = requests.get(url, cookies=cookie)
        store_data(key_name, data.text)
        text = data.text
    else:
        text = get_data(url)
        if text == None:
            data = requests.get(url, cookies=cookie)
            store_data(key_name, data.text)
            text = data.text

    print(text)
    js_dic = json.loads(text)
    return js_dic


if __name__ == "__main__":
    js = get_json_from_url("https://www.instagram.com/p/CJ8u5PCH-WG/?__a=1")
    print("js: ")
    print(js)
