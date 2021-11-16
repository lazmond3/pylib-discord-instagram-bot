from .discord_event_listener import main
from typing import List
import nest_asyncio
import os
from logging import getLogger, StreamHandler, INFO
logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


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


def mkdir_notexists(dirs: List[str]):
    for dirpath in dirs:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


if __name__ == "__main__":
    mkdir_notexists(["dumps",
                     "dump_images",
                     "dump_json"])
    env_check()
    main()
