from instagram_to_discord.sites.instagram.instagram_type import (
    convert_long_caption,
    instagram_parse_json_to_obj,
)

from .util import *


def test_convert_long_caption():
    text = """1234567890-----\n"""
    long_text = "\n".join(list(map(str, range(100))))

    assert convert_long_caption(text) == text
    assert convert_long_caption(long_text) == "\n".join(list(map(str, range(10))))


def test_converter_instagram_画像1枚のみ():
    with open("tests/data/instagram_single_image.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    assert insta_obj.media == get_media()
    assert insta_obj.is_video == is_video()
    assert insta_obj.caption == convert_long_caption(get_caption())
    assert insta_obj.profile_url == get_profile_url()
    assert insta_obj.username == get_username()
    assert insta_obj.full_name == get_full_name()
    assert insta_obj.video_url is None


def test_converter_instagram_画像複数枚():
    with open("tests/data/instagram_multiple_image.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    print(f"insta_obj: {insta_obj}")
    assert (
        insta_obj.media
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/257475923_129136066175131_1196301985725540601_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=2KhGdLKWteEAX-o4E0V&edm=AABBvjUBAAAA&ccb=7-4&oh=d2498377b4ebb9908f4a4c658ea4c84c&oe=61B25100&_nc_sid=83d603"
    )
    assert insta_obj.is_video == False
    print(f"caption: {insta_obj.caption}")
    print(f"profile_url: {insta_obj.profile_url}")
    print(f"username: {insta_obj.username}")
    print(f"full_name: {insta_obj.full_name}")
    # print(f"video_url: {insta_obj.full_name}")
    text = "Model: @gouqimixian 🇨🇳\n\n#kawaii #kawaiigirl #sexy #cute #asiangirls #chinesegirl #chinese #cosplay #sexylingerie #sexydresses"
    assert insta_obj.caption == convert_long_caption(text)
    assert (
        insta_obj.profile_url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/244062501_1746880208836643_5597722471761680772_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=6RyRWwDeUj8AX8yjCT4&edm=AABBvjUBAAAA&ccb=7-4&oh=9aec70720ecac55a0339bdfa8829fa56&oe=61B1B957&_nc_sid=83d603"
    )
    assert insta_obj.username == "shika.kamisaka"
    assert insta_obj.full_name == "Shika 神坂"
    assert insta_obj.video_url is None


def test_converter_instagram_動画複数():
    with open("tests/data/instagram_multiple_image_and_video_佐々木希.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    assert (
        insta_obj.media
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/262625889_622862275427031_6553776972827608590_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=wKQ1UkHHWSEAX-ftqTs&edm=AABBvjUBAAAA&ccb=7-4&oh=cc8273a64829f48fd3eb74862860d224&oe=61B28AC3&_nc_sid=83d603"
    )
    assert insta_obj.is_video == False
    assert insta_obj.caption == convert_long_caption("#VOCE 2022年1月号 \nオフショット💄💕")
    assert (
        insta_obj.profile_url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/24175048_1706810412710767_1281070886199230464_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=OzlpjF-F5_MAX8dMgiB&edm=AABBvjUBAAAA&ccb=7-4&oh=5184eb16de42e12178d432d6fb9ec50e&oe=61B214CF&_nc_sid=83d603"
    )
    assert insta_obj.username == "nozomisasaki_official"
    assert insta_obj.full_name == "佐々木希"
    assert insta_obj.video_url is None
    assert insta_obj.medias[0].is_video == False
    assert (
        insta_obj.medias[0].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/262625889_622862275427031_6553776972827608590_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=wKQ1UkHHWSEAX-ftqTs&edm=AABBvjUBAAAA&ccb=7-4&oh=cc8273a64829f48fd3eb74862860d224&oe=61B28AC3&_nc_sid=83d603"
    )
    assert insta_obj.medias[1].is_video == False
    assert (
        insta_obj.medias[1].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/262156110_1209783169520142_5253333853158952609_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=106&_nc_ohc=4YizEhF6sFEAX9hXcP-&tn=YQPWPKt2Dg8eBFHh&edm=AABBvjUBAAAA&ccb=7-4&oh=758bd5c12c23a427387f73fbb5641e3c&oe=61B34778&_nc_sid=83d603"
    )
    assert insta_obj.medias[2].is_video == False
    assert (
        insta_obj.medias[2].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/262606801_128754939557701_2396783096344690237_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=101&_nc_ohc=tUU4yTWb5KYAX8z3ZBP&edm=AABBvjUBAAAA&ccb=7-4&oh=31ebe6852e9894ae0f5aae5e700d7c94&oe=61B253BC&_nc_sid=83d603"
    )
    assert insta_obj.medias[3].is_video == False
    assert (
        insta_obj.medias[3].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/261786820_997893100766933_5846544217602551755_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=105&_nc_ohc=mekSubkLzS0AX9o8qk4&edm=AABBvjUBAAAA&ccb=7-4&oh=5c32470d33907be3a61ccab161c15517&oe=61B22755&_nc_sid=83d603"
    )
    assert insta_obj.medias[4].is_video == False
    assert (
        insta_obj.medias[4].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/261761439_618775952881798_7207533278913417538_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=Zcvy3BOmJBIAX-yXr9K&edm=AABBvjUBAAAA&ccb=7-4&oh=7dbb75d845c22d96a8d509503ea73404&oe=61B19BA0&_nc_sid=83d603"
    )
    assert insta_obj.medias[5].is_video == True
    assert (
        insta_obj.medias[5].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/261386033_727011278275997_1162125023463161769_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=105&_nc_ohc=I7nGK1xVrq4AX9-KCES&edm=AABBvjUBAAAA&ccb=7-4&oe=61ADD16A&oh=61c90fe531a23fa6be5a133c33068708&_nc_sid=83d603"
    )
    assert insta_obj.medias[6].is_video == True
    assert (
        insta_obj.medias[6].url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/261682859_421410326187791_5424664796032589766_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=vQAJEiO_c18AX9b99l3&edm=AABBvjUBAAAA&ccb=7-4&oe=61ADF3F3&oh=1aafe75d9e1e2160d33d489dec24eb85&_nc_sid=83d603"
    )


def test_converter_instagram_動画メイン1つ():
    with open("tests/data/instagram_single_video.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    assert (
        insta_obj.video_url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/205064059_2276556202474871_4228301026603728176_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=k8l8DhYtjCMAX9C8LNP&edm=APfKNqwBAAAA&ccb=7-4&oe=60E408DE&oh=3ff999247ea45edd802b746e6f0c6e83&_nc_sid=74f7ba"
    )


if __name__ == "__main__":
    test_converter_instagram_動画複数()
