import logging
import os
from cmreslogging.handlers import CMRESHandler

ES_HOST = os.getenv("ES_HOST")
ES_USER_NAME = os.getenv("ES_USER_NAME")
ES_PASSWORD  = os.getenv("ES_PASSWORD")
ENV = os.getenv("ENV")


if ENV != "local":
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
    log = logging.getLogger("GlobalLogger")
    # 本当は、PRODだったらsetLevel: Info とかでもよい。
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
else:
    class Log:
        def debug(self, x): print(f"[debug] {x}")
        def info(self, x): print(f"[info] {x}")
        def warning(self, x): print(f"[warning] {x}")
        def error(self, x): print(f"[error] {x}")
    log = Log()
