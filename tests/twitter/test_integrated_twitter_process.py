from instagram_to_discord import mkdir_notexists
import instagram_to_discord.cookie_requests
from instagram_to_discord.sites.instagram.converter_instagram_url import instagram_make_author_page
from instagram_to_discord.sites.twitter.twitter_process import process_twitter
from instagram_to_discord.string_util import sophisticate_string
from instagram_to_discord.util2.embed import create_instagram_pic_embed
from instagram_to_discord.util2.types import DiscordMemoClient
from instagram_to_discord.sites.instagram.instagram_process import process_instagram
import instagram_to_discord.cookie_requests
import discord
from discord.state import ConnectionState
from discord.enums import ChannelType
import pytest_mock
import pytest


@pytest.mark.asyncio
async def test_process_twitter_画像2枚目(mocker: pytest_mock.MockerFixture):
    mkdir_notexists(["dump_json_twitter"])

    client = DiscordMemoClient(
        last_url_instagram=dict(),
        last_url_twitter=dict(),
        is_twitter_last=False
    )

    data = dict({
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
        "stickers": []
    })
    state = ConnectionState(
        dispatch=None,
        handlers=None,
        hooks=None,
        syncer=None,
        http=None,
        loop=None
    )

    channel = discord.TextChannel(state=state,
                                  guild=discord.Guild(
                                      data=data,
                                      state=state
                                  ),
                                  data=data)

    message = discord.Message(
        state=state,
        data=data,
        channel=channel
    )

    content = "https://twitter.com/yoyo30g/status/1466983215714168837?s=21 2"

    with open("tests/data/twitter/dump_twitter_1466983215714168837.json") as f:
        text = f.read()

    new_urls = ["url1", "url2"]
    mocker.patch("requests.get", return_value=text)
    mocker.patch.object(instagram_to_discord.sites.twitter.twitter_process, "create_new_image_urls_with_downloading", return_value=new_urls)  # nopep8
    mocker.patch.object(instagram_to_discord.sites.twitter.twitter_process, "send_twitter_images_from_cache_for_specified_index")  # nopep8

    await process_twitter(
        client=client,
        message=message,
        content=content
    )

    assert instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.call_count == 1
    instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.assert_called_once_with(
        skip_one=True,
        image_urls=new_urls,
        nums=[2],
        message=message
    )
