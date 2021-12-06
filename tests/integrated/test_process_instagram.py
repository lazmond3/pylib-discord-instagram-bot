import discord
import pytest_mock

from instagram_to_discord.sites.instagram.instagram_process import process_instagram
from instagram_to_discord.util2.types import DiscordMemoClient


# def test_process_instagram(mocker: pytest_mock.mocker):
#     # mock = mocker.mock()

#     client = DiscordMemoClient(
#         last_url_instagram=dict(),
#         last_url_twitter=dict(),
#         is_twitter_last=False
#     )

#     channel = mocker.mock(spec=discord.TextChannel)
#     channel_mock = mocker.patch.object(channel, "send")

#     message = mocker.mock(spec=discord.Message)
#     message.channel = channel

#     content = "https://www.instagram.com/p/CW4YfYIvgHD/ 5"

#     process_instagram(
#         client=client,
#         channel=channel,
#         message=message,
#         content=content
#     )
