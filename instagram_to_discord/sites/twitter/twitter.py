from typing import List
from debug import DEBUG
import discord
from ...string_util import sophisticate_string
import re
from typing import List
from ..twitter.cli import get_one_tweet
from ..twitter.twitter_image import TwitterImage

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
        if DEBUG:
            print(f"send_twitter_image: url: {image_urls[idx]}")
        embed = create_embed_twitter_image(image_urls[idx])
        await message.channel.send(embed=embed)

def create_embed_twitter_image(image_url: str):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_image(url=image_url)
    return embed



def twitter_extract_tweet_id(line: str) -> str:
    # sample: https://twitter.com/mmmlmmm2/status/1372519422380797955?s=09
    m = re.match(r"^.*https://twitter.com/([^/]+)/status/([0-9]+).*$", line)
    if m:
        return m.group(2)
    else:
        raise Exception(f"error failed to parse re line: {line}")


def twitter_extract_tweet_url(line: str) -> str:
    # sample: https://twitter.com/mmmlmmm2/status/1372519422380797955?s=09
    m = re.match(r"^.*(https://twitter.com/([^/]+)/status/([0-9]+)).*$", line)
    if m:
        return m.group(1)
    else:
        raise Exception(f"error failed to parse re line: {line}")


def twitter_fetch_content_return_image_urls(tweet_id: str) -> List[str]:
    """get_one_tweet し、 image_urls を返す関数"""
    tw = get_one_tweet(tweet_id)
    return tw.image_urls


# TODO: extended_entities が入ってなければ、 Noneを返すようにしたい。
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
