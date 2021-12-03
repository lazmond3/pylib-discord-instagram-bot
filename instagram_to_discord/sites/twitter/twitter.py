from typing import List
import discord
import os

from instagram_to_discord.util2.embed import create_embed_twitter_image
from ...boto3 import upload_image_file

from ...download import download_file, download_file_to_path, make_twitter_image_filename, save_image
from ...params import IS_DEBUG
import re
from typing import List
from ..twitter.api import get_one_tweet
from ..twitter.twitter_image import TwitterImage


def create_new_image_urls_with_downloading(tweet_id: str, image_urls: List[str]):
    """
    image_urls を利用して、ファイルをダウンロードし、新しい image_urls (s3) に変換する。
    """
    # TODO: ここに、dynamo KVS から結果を取得し(あれば), そのキャッシュの値を返す。

    new_image_urls = []
    for idx, u in enumerate(image_urls):
        idx += 1
        fname_image = make_twitter_image_filename("dump_images", tweet_id, idx, u)
        # ファイルダウンロード
        download_file_to_path(u, fname_image)
        path = upload_image_file(fname_image, tweet_id, idx)
        new_image_urls.append(path)
        if not IS_DEBUG:
            os.remove(fname_image)
    return new_image_urls

async def send_twitter_images_from_cache_for_specified_index(
    skip_one: bool, image_urls: List[str], nums: List[int], message
):
    for n in nums:
        idx = n - 1
        assert idx >= 0
        assert idx < 4
        if len(image_urls) < n:
            continue
        if skip_one and n == 1:
            continue
        embed = create_embed_twitter_image(image_urls[idx])
        await message.channel.send(embed=embed)

def twitter_extract_tweet_id(line: str) -> str:
    """
    コンテンツ(メッセージ) の中にtwitterの URL が含まれていれば、それだけ抽出して、tweet_id を返す。
    """
    # sample: https://twitter.com/mmmlmmm2/status/1372519422380797955?s=09
    m = re.match(r"^.*https://twitter.com/([^/]+)/status/([0-9]+).*$", line, re.M)
    if m:
        return m.group(2)
    else:
        raise Exception(f"error failed to parse re line: {line}")


def twitter_extract_tweet_url(line: str) -> str:
    # sample: https://twitter.com/mmmlmmm2/status/1372519422380797955?s=09
    m = re.match(r"^.*(https://twitter.com/([^/]+)/status/([0-9]+)).*$", line, re.M)
    if m:
        return m.group(1)
    else:
        raise Exception(f"error failed to parse re line: {line}")


def twitter_fetch_content_return_image_urls(tweet_id: str) -> List[str]:
    """get_one_tweet し、 image_urls を返す関数"""
    tw = get_one_tweet(tweet_id)
    return tw.image_urls


def get_twitter_object(tweet_id: str) -> TwitterImage:
    """get_one_tweet し、 TwitterImageにする関数"""
    return get_one_tweet(tweet_id)


def twitter_line_to_image_urls(line: str) -> List[str]:
    tweet_id = twitter_extract_tweet_id(line)
    return twitter_fetch_content_return_image_urls(tweet_id)


if __name__ == "__main__":
    from sys import argv

    r = twitter_extract_tweet_id(argv[1])
    print("result: ", r)
    urls = twitter_fetch_content_return_image_urls(r)
    print(f"urls: {urls}")
