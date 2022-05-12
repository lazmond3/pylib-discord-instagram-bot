import logging
import os
from cmreslogging.handlers import CMRESHandler

ES_HOST = os.getenv("ES_HOST")
ES_USER_NAME = os.getenv("ES_USER_NAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ENV = os.getenv("ENV")


handler = CMRESHandler(
    hosts=[
        {
            "host": ES_HOST,
            "port": 443,
        }
    ],
    auth_type=CMRESHandler.AuthType.BASIC_AUTH,
    es_index_name="discord_instagram",
    use_ssl=True,
    auth_details=(ES_USER_NAME, ES_PASSWORD),
    es_additional_fields={"App": "DiscordInsta", "Environment": ENV},
)
logger = logging.getLogger("GlobalLogger")
# 本当は、PRODだったらsetLevel: Info とかでもよい。
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Log:
    def __init__(self, logger):
        self.logger = logger

    def debug(self, *x):
        self.logger.debug(*x)
        print(f"[debug] ", *x)

    def info(self, *x):
        self.logger.info(*x)
        print(f"[info] ", *x)

    def warning(self, *x):
        self.logger.warning(*x)
        print(f"[warning] ", *x)

    def error(self, *x):
        self.logger.error(*x)
        print(f"[error] ", *x)


if ENV == "local":
    log = Log(logger)
else:
    log = logger
