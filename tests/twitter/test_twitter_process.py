import os

import pytest
import pytest_mock

import instagram_to_discord.cookie_requests
from instagram_to_discord import mkdir_notexists
from instagram_to_discord.sites.twitter.api import TOKEN_FILENAME
from instagram_to_discord.sites.twitter.twitter_process import process_twitter


class Object(object):
    pass


@pytest.mark.asyncio
async def test_process_twitter_画像2枚目(mocker: pytest_mock.MockerFixture):
    mkdir_notexists(["dump_json_twitter", "dump_json"])

    client = mocker.patch("instagram_to_discord.util2.types.DiscordMemoClient")
    message = mocker.patch("discord.Message")
    content = "https://twitter.com/yoyo30g/status/1466983215714168837?s=21 2"

    with open("tests/data/twitter/dump_twitter_1466983215714168837.json") as f:
        text = f.read()

    new_urls = ["url1", "url2"]
    obj = Object()
    obj.text = text
    mocker.patch("requests.get", return_value=obj)
    mocker.patch.object(
        instagram_to_discord.sites.twitter.api, "get_auth_wrapper"
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.twitter.twitter_process,
        "create_new_image_urls_with_downloading",
        return_value=new_urls,
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.twitter.twitter_process,
        "send_twitter_images_from_cache_for_specified_index",
    )  # nopep8

    # TODO: mocker patch でなんとかならないか？ (aws の連携解除)
    instagram_to_discord.sites.twitter.api.add_json_to_dynamo_tweet_json = lambda x, y: x

    if not os.path.exists(TOKEN_FILENAME):
        with open(TOKEN_FILENAME, "w") as f:
            f.write('{"access_token": "dummy  access token"}')

    await process_twitter(client=client, message=message, content=content)

    assert (
        instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.call_count
        == 1
    )
    instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.assert_called_once_with(
        skip_one=True, image_urls=new_urls, nums=[2], message=message
    )


@pytest.mark.asyncio
async def test_process_twitter_画像1枚目_何もしない(mocker: pytest_mock.MockerFixture):
    mkdir_notexists(["dump_json_twitter"])

    client = mocker.patch("instagram_to_discord.util2.types.DiscordMemoClient")
    message = mocker.patch("discord.Message")
    content = "https://twitter.com/yoyo30g/status/1466983215714168837?s=21"

    with open("tests/data/twitter/dump_twitter_1466983215714168837.json") as f:
        text = f.read()
    obj = Object()
    obj.text = text

    new_urls = ["url1", "url2"]
    mocker.patch("requests.get", return_value=obj)
    mocker.patch.object(
        instagram_to_discord.sites.twitter.twitter_process,
        "create_new_image_urls_with_downloading",
        return_value=new_urls,
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.sites.twitter.twitter_process,
        "send_twitter_images_from_cache_for_specified_index",
    )  # nopep8
    mocker.patch.object(
        instagram_to_discord.boto3, "add_json_to_dynamo_tweet_json"
    )  # nopep8

    await process_twitter(client=client, message=message, content=content)

    assert (
        instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.call_count
        == 1
    )
    instagram_to_discord.sites.twitter.twitter_process.send_twitter_images_from_cache_for_specified_index.assert_called_once_with(
        skip_one=True, image_urls=new_urls, nums=[1], message=message
    )
