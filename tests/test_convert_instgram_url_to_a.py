# -*- coding: utf-8 -*-

# from .context import use_hello
import unittest
from . import context
from debug import DEBUG

instagram_to_discord = context.instagram_to_discord


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_instagram_make_base_url(self):
        input_str = "https://www.instagram.com/p/CGEF-ewBxNm/?utm_source=ig_web_copy_link"
        answer = "https://www.instagram.com/p/CGEF-ewBxNm"
        result = instagram_to_discord.convert_instgram_url_to_a.instagram_make_base_url(
            input_str
        )
        if DEBUG:
            print(f"answer: {answer}")
            print(f"result: {result}")
        assert answer == result

    def test_instagram_make_author_page(username):
        input_usr = "winter_28270"
        answer = "https://www.instagram.com/winter_28270/"
        result = instagram_to_discord.convert_instgram_url_to_a.instagram_make_author_page(
            input_usr)
        assert answer == result


if __name__ == '__main__':
    unittest.main()
