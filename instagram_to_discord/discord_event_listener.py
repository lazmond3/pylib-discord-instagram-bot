import discord
import os
import re
from debug import DEBUG
from instagram_type import instagran_parse_json_to_obj, InstagramData
from string_util import sophisticate_string
from converter_instagram_url import instagram_make_author_page, instagram_make_base_url


class DiscordMessageListener(discord.Client):
    def __init__(self, insta_obj: InstagramData):
        super().__init__()
        self.insta_obj = insta_obj

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    def create_embed(self, obj: InstagramData, base_url: str):
        description = sophisticate_string(obj.caption)
        embed = discord.Embed(
            title=obj.full_name,
            description=description,
            url=base_url,  # "https://www.instagram.com/p/CJ8u5PCH-WG/",
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
        if "kazami" in message.author.display_name:
            # await message.channel.send("hi message detection")
            url = "https://www.instagram.com/p/CJ8u5PCH-WG/"
            embed = self.create_embed(self.insta_obj, url)
            await message.channel.send(embed=embed)


if __name__ == "__main__":

    with open("instagram_sample_img.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagran_parse_json_to_obj(js_str)

    client = DiscordMessageListener(insta_obj)

    TOKEN = os.getenv("TOKEN")
    if DEBUG:
        print("TOKEN: ", TOKEN)
    client.run(TOKEN)
