from . import redis_cli
from . import string_util
from . import converter_instagram_url
from . import cookie_requests
from . import download
from . import youtube
import os

def env_check():
    if all([
        os.getenv("TOKEN"),
        os.getenv("CONSUMER_KEY"),
        os.getenv("CONSUMER_SECRET"),
        os.getenv("MID"),
        os.getenv("SESSIONID"),
        os.getenv("CONTAINER_TAG")
    ]):
        print("all environment variables are set.")
        print("container tag: ", os.getenv("CONTAINER_TAG"))
    else:
        print("some of required variables are not set.")
        exit(1)
    if not os.getenv("MID"):
        print("ERROR! MID NOT SET")
        exit(1)
    if not os.getenv("SESSIONID"):
        print("ERROR! SESSIONID NOT SET")
        exit(1)



from .discord_event_listener import main

if __name__ == "__main__":
    env_check()
    main()
