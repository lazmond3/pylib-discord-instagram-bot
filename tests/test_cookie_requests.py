# -*- coding: utf-8 -*-

# from .context import use_hello
import unittest
from . import context
from debug import DEBUG
instagram_to_discord = context.instagram_to_discord


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    # danger access outside
    def test_get_results(self):
        url = "https://www.instagram.com/p/CJ8u5PCH-WG/?src=hoge"
        a_url = instagram_to_discord.converter_instagram_url.convert_instagram_url_to_a(
            url)

        text = instagram_to_discord.cookie_requests.requests_get_cookie(
            url=a_url, expire=100)
        assert instagram_to_discord.redis_cli.get_data(a_url) != None


if __name__ == '__main__':
    unittest.main()
