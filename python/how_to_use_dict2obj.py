import json
from dict2obj import Dict2Obj

if __name__ == "__main__":
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