from discord import ChannelType
from discord.state import ConnectionState
import discord


def make_settings():
    data = dict(
        {
            "id": 1,
            "type": ChannelType.text,
            "name": "name",
            "position": 0,
            "attachments": [],
            "embeds": [],
            "edited_timestamp": None,
            "pinned": False,
            "mention_everyone": False,
            "tts": None,
            "content": "not true content: error",
            "nonce": None,
            "stickers": [],
        }
    )
    state = ConnectionState(
        dispatch=None, handlers=None, hooks=None, syncer=None, http=None, loop=None
    )

    channel = discord.TextChannel(
        state=state, guild=discord.Guild(data=data, state=state), data=data
    )
    return state, data, channel
