# -*- coding: utf-8 -*-

# from .context import use_hello


import json

from instagram_to_discord.sites.twitter import base64_util, twitter
# from instagram_to_discord.sites.instagram.instagram_sender import convert_long_caption
from instagram_to_discord.sites.twitter.twitter_image import convert_twitter


def test_base64():
    text = "original text"
    converted_base64 = base64_util.base64_encode_str(text)
    assert converted_base64 == "b3JpZ2luYWwgdGV4dA=="
    decoded = base64_util.base64_decode_str(converted_base64)
    assert text == decoded


def test_convert_twitter():
    fname = "tests/twitter/test_twitter_multi_image.json"
    with open(fname) as f:
        dic = json.load(f)

    tw = convert_twitter(dic)
    ans_list = [
        "https://pbs.twimg.com/media/E4n08FMVoAMrCa-.jpg",
        "https://pbs.twimg.com/media/E4n08FcUUAIyo-K.jpg",
        "https://pbs.twimg.com/media/E4n08FlUcAAmMR4.jpg",
        "https://pbs.twimg.com/media/E4n08F1UcAcqpL8.jpg",
    ]
    for i, z in zip(tw.image_urls, ans_list):
        assert i == z
    assert tw.id_str == "1407925711277486082"
    assert tw.video_url is None
    assert tw.user_display_name == "葉月"
    assert tw.user_screen_name == "hzk0207"
    assert tw.user_url == "https://twitter.com/hzk0207"
    assert (
        tw.user_profile_image_url
        == "https://pbs.twimg.com/profile_images/1407935795034411009/WU4UxW3j_normal.jpg"
    )
    assert tw.text == "おクラシックでしたの https://t.co/P2jhy4xVSJ"
