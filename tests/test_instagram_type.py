# -*- coding: utf-8 -*-
from instagram_to_discord.instagram_type import convert_long_caption
import unittest
from . import context

instagram_to_discord = context.instagram_to_discord


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_convert_long_caption(self):
        text = """1234567890-----
"""
        long_text = "\n".join(list(map(str, range(100))))

        assert convert_long_caption(text) == text
        assert convert_long_caption(long_text) == "\n".join(
            list(map(str, range(10))))


if __name__ == '__main__':
    unittest.main()
