# -*- coding: utf-8 -*-

# from .context import use_hello
from instagram_to_discord.instagram_type import convert_long_caption
import unittest
from . import context
from debug import DEBUG
instagram_to_discord = context.instagram_to_discord
twitter = context.instagram_to_discord.twitter



class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_base64(self):
        text = "original text"
        converted_base64 = twitter.base64_encode_str(text)
        assert converted_base64 == "b3JpZ2luYWwgdGV4dA=="
        decoded = twitter.base64_decode_str(converted_base64)
        assert text == decoded

if __name__ == '__main__':
    unittest.main()
