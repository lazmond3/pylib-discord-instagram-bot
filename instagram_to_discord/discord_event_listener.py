import discord
import os
import re
from debug import DEBUG
from instagram_type import instagran_parse_json_to_obj, InstagramData
from .string_util import sophisticate_string
from .converter_instagram_url import instagram_make_author_page, instagram_make_base_url, instagram_extract_from_content
from .converter_instagram_url import convert_instagram_url_to_a
from .cookie_requests import requests_get_cookie


class DiscordMessageListener(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

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

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(f"Message from {message.author.display_name}")
        print(f"\tchannel: {message.channel}")
        print(f"\ttype channel: {type(message.channel)}")
        if not "instagram-support" in \
            message.author.display_name and \
                ("https://www.instagram.com/p/" in message.content or
                 "https://www.instagram.com/reel/" in message.content):
            print("[log] channel name: ", message.channel.name)
            extracted_base_url = instagram_extract_from_content(message.content)
            if not extracted_base_url:
                print("[error] failed to parse base_url for : ", message.content)
                return
            a_url = convert_instagram_url_to_a(extracted_base_url)
            text = requests_get_cookie(url=a_url)
            insta_obj = instagran_parse_json_to_obj(text)

            embed = self.create_embed(insta_obj, extracted_base_url)
            await message.channel.send(embed=embed)
        elif not "instagram-support" in message.author.display_name and \
            ("https://twitter.com/" in message.content and
                 "/status/" in message.content):
            pass




def main():
    client = DiscordMessageListener()

    TOKEN = os.getenv("TOKEN")
    if DEBUG:
        print("TOKEN: ", TOKEN)
    client.run(TOKEN)
