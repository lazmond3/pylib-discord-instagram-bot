import json
import os
UPDATE=(os.getenv("UPDATE"))
DEBUG=(os.getenv("DEBUG"))

if __name__ == "__main__":
    js = """
    {
        "name": "test value"
    }
    """
    if DEBUG:
        print(json.loads(js))
    assert(json.loads(js) == dict({"name": "test value"}))