import discord
import os
from debug import DEBUG


class MyClient(discord.Client):
    def __init__(self):
        super().__init__()
        # kzm_channel_num = 384715340934021120
        # self.kzm_chan = self.get_channel(kzm_channel_num)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(f"Message from {message.author.display_name}")
        print(f"\tchannel: {message.channel}")
        print(f"\ttype channel: {type(message.channel)}")
        if "kazami" in message.author.display_name:
            await message.channel.send("hi message detection")


client = MyClient()
# client.run('my token goes here')

TOKEN = os.getenv("TOKEN")
if DEBUG:
    print("TOKEN: ", TOKEN)
client.run(TOKEN)
