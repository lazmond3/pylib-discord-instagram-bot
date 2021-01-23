import discord
import os
import re
from debug import DEBUG
from instagram_type import instagran_parse_json_to_obj, InstagramData
from string_util import sophisticate_string


class DiscordMessageListener(discord.Client):
    def __init__(self, insta_obj: InstagramData):
        super().__init__()
        self.insta_obj = insta_obj

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    def create_embed(self, obj: InstagramData):
        description = sophisticate_string(obj.caption)
        embed = discord.Embed(
            title="instagram",
            description=description,
            url="https://www.instagram.com/p/CJ8u5PCH-WG/",
            color=discord.Color.red()
        )
        embed.set_image(url=obj.media)
        embed.set_author(name=obj.full_name,
                         url="https://www.instagram.com/p/CJ8u5PCH-WG/",
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
            embed = self.create_embed(self.insta_obj)
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
