import os
from typing import Dict, List

import discord
from debug import DEBUG

from .boto3 import upload_video_file, upload_image_file
from .const_value import FSIZE_TARGET
from .converter_instagram_url import (convert_instagram_url_to_a,
                                      instagram_extract_from_content,
                                      instagram_make_author_page)
from .cookie_requests import requests_get_cookie
from .download import (download_file, make_instagram_mp4_filename, make_twitter_image_filename,
                       make_twitter_mp4_filename, save_image)
from .instagram_type import (InstagramData, get_multiple_medias_from_str,
                             instagran_parse_json_to_obj)
from .sites.tiktok_handler import handle_tiktok_main
from .sites.youtube_handler import handle_youtube_main
from .sites.instagram_process import process_instagram
from .sites.twitter import send_twitter_images_for_specified_index
from .sites.twitter_process import process_twitter
from .string_util import sophisticate_string
from .twitter_multiple import (get_twitter_object, twitter_extract_tweet_id,
                               twitter_extract_tweet_url,
                               twitter_line_to_image_urls)
from .util import is_int
from .video import trimming_video_to_8MB

IS_DEBUG = os.getenv("IS_DEBUG")

class DiscordMessageListener(discord.Client):
    last_url_twitter: Dict[str, str] = {}
    last_url_instagram: Dict[str, str] = {}
    is_twitter_last = True

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))



    async def on_message(self, message):
        print(
            "Message from {0.author.display_name} in ({0.channel}): {0.content}".format(
                message
            )
        )
        content = message.content
        channel = message.channel
        if IS_DEBUG and "debug" not in channel.name: return
        if not IS_DEBUG and "debug" in channel.name: return

        if "instagram-support" in message.author.display_name:
            return

        if (
            "https://www.youtube.com" in content
            or "https://youtu.be" in content
            or "https://youtube.com" in content
        ):

            print("[youtube] channel: ", channel.id)

            await handle_youtube_main(self, channel_id=channel.id, content=content)
            # p = Process(target=handle_youtube, args=(channel.id, content))
            # p.start()

        elif "https://" in content and "tiktok.com" in content:
            print("[tiktok] -> " + content, channel.id)
            await handle_tiktok_main(self, channel_id=channel.id, content=content)
            # p = Process(target=handle_tiktok, args=(channel.id, content))
            # p.start()

        elif "https://www.instagram.com/" in content and (
            "/p/" in content or "/reel/" in content
        ):
            # process instagram
            await process_instagram(self, channel, message, content)
        elif "https://twitter.com/" in content and "/status/" in content:
            await process_twitter(self, channel, message, content)
        # 数字のみ: channel に保存されたインデックスの画像を投稿する。
        elif len(list(filter(lambda x: is_int(x), content.split(",")))) > 0 and (
            channel in self.last_url_twitter or channel in self.last_url_instagram
        ):  # last_url_twitter が存在する。
            if self.is_twitter_last:
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                image_urls = twitter_line_to_image_urls(self.last_url_twitter[channel])
                await send_twitter_images_for_specified_index(
                    skip_one=True, image_urls=image_urls, nums=nums, message=message
                )  # 動画のサムネイル送信
            else:  # instagram
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                text = requests_get_cookie(url=self.last_url_instagram[channel])
                image_urls = get_multiple_medias_from_str(text)
                await send_twitter_images_for_specified_index(
                    skip_one=False, image_urls=image_urls, nums=nums, message=message
                )  # 動画のサムネイル送信


def main():
    client = DiscordMessageListener()

    TOKEN = os.getenv("TOKEN")
    if DEBUG and TOKEN:
        print("TOKEN: ", TOKEN[0:4] + "....." + TOKEN[-3:])
    client.run(TOKEN)
