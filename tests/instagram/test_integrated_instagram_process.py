import discord
import pytest
import pytest_mock
from discord.enums import ChannelType
from discord.state import ConnectionState

import instagram_to_discord.cookie_requests
from instagram_to_discord import mkdir_notexists
from instagram_to_discord.sites.instagram.converter_instagram_url import \
    instagram_make_author_page
from instagram_to_discord.sites.instagram.instagram_process import \
    process_instagram
from instagram_to_discord.string_util import sophisticate_string
from instagram_to_discord.util2.embed import create_instagram_pic_embed
from instagram_to_discord.util2.types import DiscordMemoClient

from .util import make_settings


@pytest.mark.asyncio
async def test_process_instagram(mocker: pytest_mock.MockerFixture):
    mkdir_notexists(["dump_json_instagram"])
    client = mocker.patch("instagram_to_discord.util2.types.DiscordMemoClient")

    state, data, channel = make_settings()

    message = discord.Message(state=state, data=data, channel=channel)

    content = "https://www.instagram.com/p/CW4YfYIvgHD/ 5"

    text = ""
    with open("tests/data/instagram_multiple_image_and_video_new_佐々木.json") as f:
        text = f.read()
    mock_image_url = "dummy_url"

    # 一応作ってるけど mock です。
    embed = discord.Embed(
        title="佐々木希",
        description=sophisticate_string("#VOCE 2022年1月号 \nオフショット💄💕"),
        url="https://www.instagram.com/p/CW4YfYIvgHD",
        color=discord.Color.red(),
    )
    embed.set_image(url=mock_image_url)
    embed.set_author(
        name="佐々木希",
        url=instagram_make_author_page("nozomisasaki_official"),
        icon_url="https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/24175048_1706810412710767_1281070886199230464_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=OzlpjF-F5_MAX_zYlhx&edm=AABBvjUBAAAA&ccb=7-4&oh=6954b174179012577379e144883a0456&oe=61B40F0F&_nc_sid=83d603",
    )

    # 何もしないが、あとで embed で呼ばれたか確認する。
    mocker.patch.object(discord.abc.Messageable, "send")
    # 何もしないようにする (dynamo put)
    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process,
        "add_instagram_json_to_dynamo_instagram_json",
    )  # nopep8

    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process,
        "requests_get_cookie",
        return_value=text,
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process, "save_image"
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process, "download_file"
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process,
        "upload_image_file",
        return_value=mock_image_url,
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.instagram.instagram_process,
        "create_instagram_pic_embed",
        return_value=embed,
    )  # nopep8
    mocker.patch("os.remove")

    await process_instagram(client=client, message=message, content=content)

    # discord.abc.Messageable.send.assert_called_once_with(embed)
    assert discord.abc.Messageable.send.call_count == 1
    discord.abc.Messageable.send.assert_called_once_with(embed=embed)


if __name__ == "__main__":
    test_process_instagram()
