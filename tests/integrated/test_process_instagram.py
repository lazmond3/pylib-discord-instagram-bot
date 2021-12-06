import discord
import pytest_mock

from instagram_to_discord.sites.instagram.instagram_process import process_instagram
from instagram_to_discord.util2.types import DiscordMemoClient


def test_process_instagram(mocker: pytest_mock.MockerFixture):
    # mock = mocker.mock()

    client = DiscordMemoClient(
        last_url_instagram=dict(),
        last_url_twitter=dict(),
        is_twitter_last=False
    )

    channel = discord.TextChannel()
    channel_spy = mocker.spy(channel, "message")
    channel_spy = mocker.spy(channel, "send")

    message = discord.Message(channel=channel)
    message_spy = mocker.spy(message)

    message.channel = channel

    # channel = mocker.mock(spec=discord.TextChannel)
    # channel_mock = mocker.patch.object(channel, "send")

    # message = mocker.mock(spec=discord.Message)

    content = "https://www.instagram.com/p/CW4YfYIvgHD/ 5"

    process_instagram(
        client=client,
        channel=channel,
        message=message,
        content=content
    )


if __name__ == "__main__":
    test_process_instagram()
