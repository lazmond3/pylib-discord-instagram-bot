import os
from .logging import log as logger
from typing import List

# これなんで入れてるんだっけ
from .discord_event_listener import main  # noqa: F401

FSIZE_TARGET = 2**23 - 100


def env_check():
    if all(
        [
            os.getenv("TOKEN"),
            os.getenv("CONSUMER_KEY"),
            os.getenv("CONSUMER_SECRET"),
            os.getenv("MID"),
            os.getenv("SESSIONID"),
            os.getenv("ENV"),
            # elasticsearch is not necessary.
            # os.getenv("ES_HOST"),
            # os.getenv("ES_USER_NAME"),
            # os.getenv("ES_PASSWORD"),
        ]
    ):
        logger.info("all environment variables are set.")
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
