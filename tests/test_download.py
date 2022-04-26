# -*- coding: utf-8 -*-

# from .context import use_hello
import json
import unittest

from instagram_to_discord.download import make_instagram_mp4_filename
from instagram_to_discord.sites.instagram.instagram_type import \
    convert_long_caption
from instagram_to_discord.sites.twitter.twitter_image import convert_twitter


def test_make_instagram_mp4_filename():
    url = "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/205064059_2276556202474871_4228301026603728176_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=k8l8DhYtjCMAX9C8LNP&edm=APfKNqwBAAAA&ccb=7-4&oe=60E408DE&oh=3ff999247ea45edd802b746e6f0c6e83&_nc_sid=74f7ba"
    fname = make_instagram_mp4_filename(base_dir="", url=url)
    assert fname == "205064059_2276556202474871_4228301026603728176_n.mp4"
