import discord
import os
import re
from debug import DEBUG
from instagram_type import instagran_parse_json_to_obj, InstagramData
from .string_util import sophisticate_string
from .converter_instagram_url import instagram_make_author_page, instagram_make_base_url, instagram_extract_from_content
from .converter_instagram_url import convert_instagram_url_to_a
from .cookie_requests import requests_get_cookie
from .twitter_multiple import twitter_line_to_image_urls, twitter_extract_tweet_url
from .util import is_int
from typing import Dict, List
class DiscordMessageListener(discord.Client):
    last_url_twitter: Dict[str, str] = {}

    def __init__(self):
        super().__init__()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def send_twitter_images_for_specified_index(self, image_urls: List[str], nums: List[int], message):
        for n in nums:
            idx = n-1
            assert(idx >= 0)
            assert(idx < 4)
            if len(image_urls) < n:
                continue
            if n == 1: continue
            if DEBUG:
                print(f"send_twitter_image: url: {image_urls[idx]}")
            embed = self.create_embed_twitter_image(image_urls[idx])
            await message.channel.send(embed=embed)


    def create_embed(self, obj: InstagramData, base_url: str):
        description = sophisticate_string(obj.caption)
        embed = discord.Embed(
            title=obj.full_name,
            description=description,
            url=base_url,
            color=discord.Color.red()
        )
        embed.set_image(url=obj.media)
        embed.set_author(name=obj.full_name,
                         url=instagram_make_author_page(obj.username),
                         icon_url=obj.profile_url
                         )
        return embed

    def create_embed_twitter_image(self, image_url: str):
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        return embed

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(f"Message from {message.author.display_name}")
        print(f"\tchannel: {message.channel}")
        print(f"\ttype channel: {type(message.channel)}")
        content = message.content
        channel = message.channel

        if "instagram-support" in message.author.display_name: return

        if ("https://www.instagram.com/p/" in content or
                 "https://www.instagram.com/reel/" in content):
            print("[log] channel name: ", message.channel.name)
            extracted_base_url = instagram_extract_from_content(content)
            if not extracted_base_url:
                print("[error] failed to parse base_url for : ", content)
                return
            a_url = convert_instagram_url_to_a(extracted_base_url)
            text = requests_get_cookie(url=a_url)
            insta_obj = instagran_parse_json_to_obj(text)

            embed = self.create_embed(insta_obj, extracted_base_url)
            await message.channel.send(embed=embed)
        elif ("https://twitter.com/" in content and "/status/" in content):
            # ここで最後のtwitter url を記録しておく。
            if DEBUG:
                print("記録する！")
            self.last_url_twitter[channel] = twitter_extract_tweet_url(content)

            msg_list = content.split()
            if len(msg_list) > 1:
                nums = msg_list[1].split(",")
                nums = map(lambda x: int(x), nums)
                nums = filter(lambda x: x != 1, nums)
                nums = list(nums)
            else: return
            image_urls = twitter_line_to_image_urls(content)
            await self.send_twitter_images_for_specified_index(image_urls, nums, message)
        elif len(list(filter(lambda x: is_int(x), content.split(",")))) > 0 and \
               self.last_url_twitter[channel]: # last_url_twitter が存在する。
            nums = list(map(lambda x: int(x), filter(lambda x: is_int(x), content.split(","))))
            image_urls = twitter_line_to_image_urls(self.last_url_twitter[channel])
            await self.send_twitter_images_for_specified_index(image_urls, nums, message)

def main():
    client = DiscordMessageListener()

    TOKEN = os.getenv("TOKEN")
    if DEBUG and TOKEN:
        print("TOKEN: ", TOKEN[0:4] + "....." + TOKEN[-3:])
    client.run(TOKEN)

    # backup history
    # import discord
    # from discord.ext import commands
    # import asyncio

    # bot = commands.Bot(command_prefix = "{")

    # @bot.command(name="clear", pass_context = True)
    # async def clear(ctx, number):
    #     number = int(number) #Converting the amount of messages to delete to an integer
    #     counter = 0
    #     print("bot command")
    #     async for x in bot.logs_from(ctx.message.channel, limit = number):
    #         if counter < number:
    #             # await Client.delete_message(x)
    #             await print(f"x: {x}")
    #             counter += 1
    #             await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even


    # @bot.command(name="copy")
    # async def copy(ctx):
    #     print(f"copy executed!: ctx: {ctx}")
    #     with open("file.txt", "w") as f:
    #         async for message in ctx.history(limit=1000):
    #             f.write(message.content + "\n")

    #     await ctx.send("Done!")
    # bot.run(TOKEN)