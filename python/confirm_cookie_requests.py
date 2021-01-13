import requests
import json

# cookie2.txt をこのように使うと、クッキーを使ったリクエストができるっぽい！
# TODO: これを吐き出す関数を作る

cookie = dict()
with open("cookie2.txt") as f:
    alltext = []
    for line in f.readlines():
        alltext.append(line.strip())
    text = "".join(alltext)
    splited = text.split("; ")
    for each in splited:
        print("split: ", each.split("="))
        key,v = each.split("=")[0], "".join(each.split("=")[1:])
        cookie[key] = v

# with open("cookies.json") as f:
#     p = json.load(f)
#     cookie = dict()
#     for i in p:
#         cookie[i["name"]] = i["value"]

print("cookie:" , cookie)

result = requests.get("https://instagram.com/", cookies = cookie)

print(result)
with open("result.html", "w") as f:
    f.write(result.text)
print(result.text)