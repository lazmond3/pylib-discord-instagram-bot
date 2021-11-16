from logging import getLogger,StreamHandler,INFO
logger = getLogger(__name__)    #以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

from typing import List
import discord
from .instagram_type import InstagramData
from ...string_util import sophisticate_string
from .converter_instagram_url import instagram_make_author_page
from ...params import IS_DEBUG

def create_embed_instagram_image(image_url: str):
    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=image_url)
    return embed

async def send_instagram_images_from_cache_for_specified_index(
    skip_one: bool, image_urls: List[str], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        if len(image_urls) < n:
            continue
        if skip_one and n == 1:
            continue
        if IS_DEBUG:
            logger.debug(f"send_twitter_image: url: {image_urls[idx]}")
        embed = create_embed_instagram_image(image_urls[idx])
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
        embed = create_embed_instagram_image(image_urls[idx])
        await message.channel.send(embed=embed)

def create_instagram_pic_embed(obj: InstagramData, base_url: str):
    description = sophisticate_string(obj.caption)
    embed = discord.Embed(
        title=obj.full_name,
        description=description,
        url=base_url,
        color=discord.Color.red(),
    )
    embed.set_image(url=obj.media)
    embed.set_author(
        name=obj.full_name,
        url=instagram_make_author_page(obj.username),
        icon_url=obj.profile_url,
    )
    return embed

def create_instagram_video_embed(obj: InstagramData, base_url: str):
    description = sophisticate_string(obj.caption)
    embed = discord.Embed(
        title=obj.full_name,
        description=description,
        url=base_url,
        color=discord.Color.red(),
    )
    embed.set_author(
        name=obj.full_name,
        url=instagram_make_author_page(obj.username),
        icon_url=obj.profile_url,
    )
    return embed
