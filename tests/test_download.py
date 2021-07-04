# -*- coding: utf-8 -*-

# from .context import use_hello
from instagram_to_discord.twitter.twitter_image import convert_twitter
from instagram_to_discord.instagram_type import convert_long_caption
import unittest
from . import context
from debug import DEBUG
instagram_to_discord = context.instagram_to_discord
twitter = context.instagram_to_discord.twitter
download = context.instagram_to_discord.download

import json


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_make_instagram_mp4_filename(self):
        url = "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/205064059_2276556202474871_4228301026603728176_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=k8l8DhYtjCMAX9C8LNP&edm=APfKNqwBAAAA&ccb=7-4&oe=60E408DE&oh=3ff999247ea45edd802b746e6f0c6e83&_nc_sid=74f7ba"
        fname = download.make_instagram_mp4_filename(base_dir="", url = url)
        assert fname == "205064059_2276556202474871_4228301026603728176_n.mp4"
if __name__ == '__main__':
    unittest.main()
