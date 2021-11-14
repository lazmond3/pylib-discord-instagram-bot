from typing import List
from debug import DEBUG
import discord


def create_embed_instagram_image(image_url: str):
    embed = discord.Embed(color=discord.Color.red())
    embed.set_image(url=image_url)
    return embed

async def send_instagram_images_for_specified_index(
    image_urls: List[str], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        if len(image_urls) < n:
            continue
        if DEBUG:
            print(f"send_twitter_image: url: {image_urls[idx]}")
        embed = create_embed_instagram_image(image_urls[idx])
        await message.channel.send(embed=embed)