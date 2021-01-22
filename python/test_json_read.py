import json
import os
UPDATE=(os.getenv("UPDATE"))
DEBUG=(os.getenv("DEBUG"))

def test_easy():
    js = """
    {
        "name": "test value"
    }
    """
    if DEBUG:
        print(json.loads(js))
    assert(json.loads(js) == dict({"name": "test value"}))

if __name__ == "__main__":
    with open("out.json") as f:
        text = "".join([x for x in f.readlines()])
        if DEBUG:
            print(text[:1000])
        
        js = json.loads(text)
        if DEBUG:
            print("js object:")
            print(js)
            print("js object:")
