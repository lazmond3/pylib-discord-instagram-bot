from logging import getLogger,StreamHandler,INFO
logger = getLogger(__name__)    #以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

import os

import nest_asyncio

from .discord_event_listener import main

nest_asyncio.apply()
FSIZE_TARGET = 2 ** 23 - 100


def env_check():
    if all(
        [
            os.getenv("TOKEN"),
            os.getenv("CONSUMER_KEY"),
            os.getenv("CONSUMER_SECRET"),
            os.getenv("MID"),
            os.getenv("SESSIONID"),
        ]
    ):
        logger.error("all environment variables are set.")
        logger.error("container tag: ", os.getenv("CONTAINER_TAG"))
    else:
        logger.error("some of required variables are not set.")
        exit(1)
    if not os.getenv("MID"):
        logger.error("ERROR! MID NOT SET")
        exit(1)
    if not os.getenv("SESSIONID"):
        logger.error("ERROR! SESSIONID NOT SET")
        exit(1)


if __name__ == "__main__":
    env_check()
    main()
