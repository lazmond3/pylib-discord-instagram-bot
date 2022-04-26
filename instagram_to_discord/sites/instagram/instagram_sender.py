from logging import INFO, StreamHandler, getLogger
from typing import List

import discord

from instagram_to_discord.sites.instagram.instagram_type import \
    InstagramInnerNode
from instagram_to_discord.sites.instagram.upload_video import \
    upload_instagram_video
from instagram_to_discord.util2.embed import create_instagram_embed_image

from ...const_value import IS_DEBUG

logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


async def send_instagram_images_from_cache_for_specified_index(
    skip_one: bool, medias: List[InstagramInnerNode], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        if len(medias) < n:
            continue
        if skip_one and n == 1:
            continue
        if IS_DEBUG:
            logger.debug(f"send_twitter_image: url: {medias[idx]}")
        m = medias[idx]
        if m.is_video:
            uploaded_video_url = upload_instagram_video(m.url)
            await message.channel.send(uploaded_video_url)
            # await message.channel.send(file=discord.File(uploaded_video_url))
        else:
            embed = create_instagram_embed_image(medias[idx].url)
            await message.channel.send(embed=embed)


def get_instagram_id_from_url(instagram_url: str):
    instagram_id = ""
    if "/p/" in instagram_url:
        instagram_id = instagram_url.split("/p/")[1].split("/")[0]
    elif "/reel/" in instagram_url:
        instagram_id = instagram_url.split("/reel/")[1].split("/")[0]
    return instagram_id


async def send_instagram_images_for_specified_index(
    image_urls: List[str], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        if len(image_urls) < n:
            continue
        if IS_DEBUG:
            logger.debug(f"send_twitter_image: url: {image_urls[idx]}")
        embed = create_instagram_embed_image(image_urls[idx])
        await message.channel.send(embed=embed)
