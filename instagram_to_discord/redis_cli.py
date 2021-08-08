# import redis
import os

from debug import DEBUG
from rediscluster import RedisCluster

REDIS_PASS = os.getenv("REDIS_PASS")
if REDIS_PASS:
    startup_nodes = [{"host": "localhost", "port": "7000", "password": REDIS_PASS}]
    rcli = RedisCluster(
        startup_nodes=startup_nodes, decode_responses=True, password=REDIS_PASS
    )

    # redis でできること
    # https://weblabo.oscasierra.net/python/python-redis-py-1.html

    def store_data(key, value, expire=None):
        rcli.set(key, value, ex=expire)

    def get_data(key):
        return rcli.get(key)

    if __name__ == "__main__":
        store_data(
            "test",
            """
        こんにちは！
        WOW
        """,
            100,
        )
        if DEBUG:
            print(get_data("test"))
        assert (
            get_data("test")
            == """
        こんにちは！
        WOW
        """
        )
        assert not get_data("test2")
