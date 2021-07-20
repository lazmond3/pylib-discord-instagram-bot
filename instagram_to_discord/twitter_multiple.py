import re
from typing import List

from debug import DEBUG

# from twitter_cli import get_one_tweet, TwitterImage
from .twitter.cli import get_one_tweet
from .twitter.twitter_image import TwitterImage


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


def twitter_fetch_content(tweet_id: str) -> List[str]:
    tw = get_one_tweet(tweet_id)
    return tw.image_urls


def get_twitter_object(tweet_id: str) -> TwitterImage:
    return get_one_tweet(tweet_id)


def twitter_line_to_image_urls(line: str) -> List[str]:
    tweet_id = twitter_extract_tweet_id(line)
    return twitter_fetch_content(tweet_id)


if __name__ == "__main__":
    from sys import argv

    r = twitter_extract_tweet_id(argv[1])
    print("result: ", r)
    urls = twitter_fetch_content(r)
    print(f"urls: {urls}")
