# -*- coding: utf-8 -*-

from instagram_to_discord.sites.instagram import converter_instagram_url


def test_instagram_make_base_url():
    input_str = (
        "https://www.instagram.com/p/CGEF-ewBxNm/?utm_source=ig_web_copy_link"
    )
    answer = "https://www.instagram.com/p/CGEF-ewBxNm"
    result = converter_instagram_url.instagram_make_base_url(
        input_str
    )
    assert answer == result


def test_instagram_make_author_page():
    input_usr = "winter_28270"
    answer = "https://www.instagram.com/winter_28270/"
    result = (
        converter_instagram_url.instagram_make_author_page(
            input_usr
        )
    )
    assert answer == result


def test_extract_from_content():
    input_content = """
        こんにちは。データは https://www.instagram.com/p/CGEF-ewBxNm/?utm_source=ig_web_copy_link です。
    """
    answer = "https://www.instagram.com/p/CGEF-ewBxNm"
    result = (
        converter_instagram_url.instagram_extract_from_content(
            input_content
        )
    )
    assert result == answer


def test_extract_url():
    input_content = """こんにちは。データは https://www.instagram.com/p/CGEF-ewBxNm/?utm_source=ig_web_copy_link です。"""
    answer = "https://www.instagram.com/p/CGEF-ewBxNm"
    result = converter_instagram_url.extract_url(
        input_content)
    assert answer == result
