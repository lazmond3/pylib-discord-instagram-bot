# -*- coding: utf-8 -*-

# from .context import use_hello
from instagram_to_discord.cookie_requests import REDIS_PASS
import unittest
from . import context
from debug import DEBUG
import requests
instagram_to_discord = context.instagram_to_discord


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    # danger access outside
    def test_get_results(self):
        url = "https://www.instagram.com/p/CJ8u5PCH-WG/?src=hoge"
        a_url = instagram_to_discord.converter_instagram_url.convert_instagram_url_to_a(
            url)

        if REDIS_PASS:
            text = instagram_to_discord.cookie_requests.requests_get_cookie(
                url=a_url, expire=100)
            assert instagram_to_discord.redis_cli.get_data(a_url) != None
        else:
            assert True


    @unittest.skip("外部ネットワークへのアクセス")
    def test_cookie(self):
        path = "cookie2.txt"
        cookie = instagram_to_discord.cookie_requests.make_cookie(path)
        text = requests.get(
            "https://www.instagram.com/p/CJ8u5PCH-WG/?__a=1",
            cookies=cookie).text
        if DEBUG:
            print("text: ", text[:300])
            print("debug test_cookie: ",
                  cookie)
        assert "graphql" in text


if __name__ == '__main__':
    unittest.main()
