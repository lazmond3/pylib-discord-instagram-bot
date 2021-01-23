import discord
import os
import re
from debug import DEBUG
from instagram_type import instagran_parse_json_to_obj, InstagramData


def sophisticate_string(st):
    st_list = st.strip().split("\n")
    if DEBUG:
        print("splited st list: ", st_list)
    new_lst = []
    for ste in st_list:
        ste = ste.strip()
        st = re.sub(r"^.[ \t\n]*$", "", ste)
        new_lst.append(st)
    new_lst = list(filter(lambda x: len(x) != 0, new_lst))
    if DEBUG:
        print("new_lst: ", new_lst)
    st = "\n".join(new_lst)
    return re.sub(r"\n\n\n+", "\n\n", st)


class MyClient(discord.Client):
    def __init__(self, instaObj: InstagramData):
        super().__init__()
        self.instaObj = instaObj
        # kzm_channel_num = 384715340934021120
        # self.kzm_chan = self.get_channel(kzm_channel_num)

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
            embed = self.create_embed(self.instaObj)
            await message.channel.send(embed=embed)


if __name__ == "__main__":

    with open("instagram_sample_img.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagran_parse_json_to_obj(js_str)

    client = MyClient(insta_obj)

    TOKEN = os.getenv("TOKEN")
    if DEBUG:
        print("TOKEN: ", TOKEN)
    client.run(TOKEN)
