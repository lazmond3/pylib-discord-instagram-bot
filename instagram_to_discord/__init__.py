import os
from logging import INFO, StreamHandler, getLogger
from typing import List

import nest_asyncio

from .discord_event_listener import main  # noqa: F401

logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


nest_asyncio.apply()
FSIZE_TARGET = 2**23 - 100


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
            logger.info(f"[mkdir_noexists] mkdir {dirpath}")
