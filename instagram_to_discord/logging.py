import logging
import os
from cmreslogging.handlers import CMRESHandler

ES_HOST = os.getenv("ES_HOST")
ES_USER_NAME = os.getenv("ES_USER_NAME")
ES_PASSWORD  = os.getenv("ES_PASSWORD")

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
    es_additional_fields={"App": "DiscordInsta", "Environment": "Dev"},
)
log = logging.getLogger("GlobalLogger")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
