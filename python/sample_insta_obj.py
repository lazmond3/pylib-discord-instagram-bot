import json
from dict2obj import Dict2Obj
with open("instagram_sample_img.json") as f:
    text = "".join([x for x in f.readlines()])
js = json.loads(text)
sample_isnta_obj = Dict2Obj(js)

