from typing import Dict

import discord

from instagram_to_discord.sites.instagram.instagram_sender import (
    send_instagram_images_from_cache_for_specified_index,
)

from .const_value import DISCORD_TOKEN, IS_DEBUG
from .cookie_requests import requests_get_cookie
from .sites.instagram.instagram_process import process_instagram
from .sites.instagram.instagram_type import get_multiple_medias_v3_from_str
from .sites.tiktok.tiktok_handler import handle_tiktok_main
from .sites.twitter.twitter import (
    send_twitter_images_from_cache_for_specified_index,
    twitter_line_to_image_urls,
)
from .sites.twitter.twitter_process import process_twitter, process_twitter_open
from .sites.youtube.youtube_handler import handle_youtube_main
from .logging import log as logger


def is_int(s):
    try:
        int(s)
    except Exception as e:  # noqa: F841
        return False
    return True


class DiscordMessageListener(discord.Client):
    last_url_twitter: Dict[discord.TextChannel, str] = {}
    last_url_instagram: Dict[str, str] = {}
    is_twitter_last = True

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        logger.info(f"Logged on as {self.user}!")

    async def on_message(self, message):
        logger.info(
            "Message from {0.author.display_name} in ({0.channel}): {0.content}".format(
                message
            )
        )
        content: str = message.content
        channel: discord.TextChannel = message.channel

        if IS_DEBUG and "debug" not in channel.name:
            return
        if not IS_DEBUG and "debug" in channel.name:
            return

        if "instagram-support" in message.author.display_name:
            return

        if (
            "https://www.youtube.com" in content
            or "https://youtu.be" in content
            or "https://youtube.com" in content
        ):

            logger.info(f"[youtube] channel: {channel.id}")
            await handle_youtube_main(self, channel_id=channel.id, content=content)

        elif "https://" in content and "tiktok.com" in content:
            logger.info(f"[tiktok] -> {content} chanid: {channel.id}")
            await handle_tiktok_main(self, channel_id=channel.id, content=content)
            # 今後SQSに投げて functions で処理していく

        elif "https://www.instagram.com/" in content and (
            "/p/" in content or "/reel/" in content
        ):  # TODO: stories などの対応を加える。
            # ここで instagram_id を出した方がいい, a_url も
            await process_instagram(self, message, content)

        elif "https://twitter.com/" in content and "/status/" in content:
            await process_twitter(self, message, content)

        # 数字のみ: channel に保存されたインデックスの画像を投稿する。
        elif len(list(filter(lambda x: is_int(x), content.split(",")))) > 0 and (
            channel in self.last_url_twitter or channel in self.last_url_instagram
        ):

            # last_url_twitter が存在する。
            if self.is_twitter_last:
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                image_urls = twitter_line_to_image_urls(self.last_url_twitter[channel])
                await send_twitter_images_from_cache_for_specified_index(
                    skip_one=True, image_urls=image_urls, nums=nums, message=message
                )  # 動画のサムネイル送信

            else:
                # TODO: cache した 画像データ から、こちらの images を取得するようにする。
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                nums = sorted(nums)

                text = requests_get_cookie(url=self.last_url_instagram[channel])
                medias = get_multiple_medias_v3_from_str(text)

                await send_instagram_images_from_cache_for_specified_index(
                    skip_one=False, medias=medias, nums=nums, message=message
                )

        elif content == "o":
            if self.is_twitter_last:
                await process_twitter_open(
                    message=message, twitter_url=self.last_url_twitter[channel]
                )


def main():
    client = DiscordMessageListener()

    if IS_DEBUG and DISCORD_TOKEN:
        logger.info(f"TOKEN: {DISCORD_TOKEN[0:4]}.....{DISCORD_TOKEN[-3:]}")
    client.run(DISCORD_TOKEN)
