import json

from debug import DEBUG

class Dict2Obj(object):
    """dict to Dict2Obj
    d: data"""

    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Dict2Obj(x) if isinstance(
                    x, dict) else x for x in b])
            else:
                setattr(self, a, Dict2Obj(b) if isinstance(b, dict) else b)


def test1():
    sample_str = """
    [
        {
            "name": "mid",
            "value": "X_-B7QAEAAEPvAmD51hvJzbC4I5i",
            "domain": ".instagram.com",
            "path": "/",
            "expires": 1673652461.509606,
            "size": 31,
            "httpOnly": false,
            "secure": true,
            "session": false
        },
        {
            "name": "urlgen",
            "value": "sample",
            "domain": ".instagram.com",
            "path": "/",
            "expires": -1,
            "size": 93,
            "httpOnly": true,
            "secure": true,
            "session": true
        }
    ]
    """
    dic =  json.loads(sample_str)
    # print("dic items: ", dic.items())
    for e in dic:
        obj = Dict2Obj(e)
        print(obj.name)
        print(obj.value)
        print(obj.domain)
        print(obj.path)
    # print(obj)
    # print(obj[0])

if __name__ == "__main__":
    with open("out.json") as f:
        text = "".join([x for x in f.readlines()])
    js = json.loads(text)
    oj = Dict2Obj(js)
    if DEBUG:
        print(oj.graphql.shortcode_media.display_url)
        print(oj.graphql.shortcode_media.edge_media_to_caption.edges[0].node.text)
        print(oj.graphql.shortcode_media.is_video)
        print(oj.graphql.shortcode_media.owner.profile_pic_url)
        print(oj.graphql.shortcode_media.owner.username)
        print(oj.graphql.shortcode_media.owner.full_name)
    