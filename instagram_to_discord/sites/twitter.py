from typing import List
from debug import DEBUG
import discord
from ..string_util import sophisticate_string

async def send_twitter_images_for_specified_index(
    skip_one: bool, image_urls: List[str], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        assert idx < 4
        if len(image_urls) < n:
            continue
        if skip_one and n == 1:
            continue
        if DEBUG:
            print(f"send_twitter_image: url: {image_urls[idx]}")
        embed = create_embed_twitter_image(image_urls[idx])
        await message.channel.send(embed=embed)

def create_embed_twitter_image(image_url: str):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_image(url=image_url)
    return embed
