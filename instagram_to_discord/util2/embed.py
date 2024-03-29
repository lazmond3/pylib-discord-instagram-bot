from typing import Optional

import discord

from instagram_to_discord.sites.instagram.converter_instagram_url import (
    instagram_make_author_page,
)
from instagram_to_discord.sites.instagram.instagram_type import InstagramData
from instagram_to_discord.sites.twitter.twitter_image import TwitterImage
from instagram_to_discord.string_util import sophisticate_string


def create_ask_embed(question: str, answer: str, url: str):
    description = f"""Q.{question}\n\nA. {answer}"""
    embed = discord.Embed(
        title="koba",
        description=description,
        url=url,
        color=discord.Color.green(),
    )
    embed.set_author(
        name="koba31okm",
        url="https://twitter.com/koba31okm",
        icon_url="https://pbs.twimg.com/profile_images/1372691769469460486/9Ug_QMow_400x400.jpg",
    )
    return embed


def create_instagram_pic_embed(obj: InstagramData, base_url: str) -> discord.Embed:
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


def create_instagram_embed_image(image_url: str):
    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=image_url)
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


def create_twitter_image_embed(image_url: str):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_image(url=image_url)
    return embed


def create_twitter_description_image(
    tw: TwitterImage, image_url: Optional[str] = None
) -> discord.Embed:
    embed = discord.Embed(
        title=tw.user_display_name,
        description=tw.text,
        url=f"https://twitter.com/{tw.user_screen_name}",
        color=discord.Color.blue(),
    )
    if image_url:
        embed.set_image(url=image_url)
    embed.set_author(
        name=tw.user_display_name,
        url=f"https://twitter.com/{tw.user_screen_name}",
        icon_url=tw.user_profile_image_url,
    )
    return embed
