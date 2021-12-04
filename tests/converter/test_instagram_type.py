from instagram_to_discord.sites.instagram.instagram_type import convert_long_caption, instagram_parse_json_to_obj

from .util import *


def test_convert_long_caption():
    text = """1234567890-----\n"""
    long_text = "\n".join(list(map(str, range(100))))

    assert convert_long_caption(text) == text
    assert convert_long_caption(long_text) == "\n".join(
        list(map(str, range(10))))


def test_converter_instagram_画像1枚のみ():
    with open("tests/instagram/instagram_single_image.json") as f:
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
    with open("tests/instagram/instagram_multiple_image.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    print(f"insta_obj: {insta_obj}")
    assert insta_obj.media == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/257475923_129136066175131_1196301985725540601_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=2KhGdLKWteEAX-o4E0V&edm=AABBvjUBAAAA&ccb=7-4&oh=d2498377b4ebb9908f4a4c658ea4c84c&oe=61B25100&_nc_sid=83d603"
    assert insta_obj.is_video == False
    print(f"caption: {insta_obj.caption}")
    print(f"profile_url: {insta_obj.profile_url}")
    print(f"username: {insta_obj.username}")
    print(f"full_name: {insta_obj.full_name}")
    # print(f"video_url: {insta_obj.full_name}")
    text = "Model: @gouqimixian 🇨🇳\n\n#kawaii #kawaiigirl #sexy #cute #asiangirls #chinesegirl #chinese #cosplay #sexylingerie #sexydresses"
    assert insta_obj.caption == convert_long_caption(text)
    assert insta_obj.profile_url == "https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/244062501_1746880208836643_5597722471761680772_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=6RyRWwDeUj8AX8yjCT4&edm=AABBvjUBAAAA&ccb=7-4&oh=9aec70720ecac55a0339bdfa8829fa56&oe=61B1B957&_nc_sid=83d603"
    assert insta_obj.username == "shika.kamisaka"
    assert insta_obj.full_name == "Shika 神坂"
    assert insta_obj.video_url is None

# TODO 未対応
# def test_converter_instagram_動画複数():
#     with open("tests/instagram/instagram_multiple_image_and_video_佐々木希.json") as f:
#         js_str = "".join(f.readlines())
#     insta_obj = instagram_parse_json_to_obj(js_str)
#     assert insta_obj.media == get_media()
#     assert insta_obj.is_video == is_video()
#     assert insta_obj.caption == convert_long_caption(get_caption())
#     assert insta_obj.profile_url == get_profile_url()
#     assert insta_obj.username == get_username()
#     assert insta_obj.full_name == get_full_name()
#     assert insta_obj.video_url is None


def test_converter_instagram_動画メイン1つ():
    with open("tests/instagram/instagram_single_video.json") as f:
        js_str = "".join(f.readlines())
    insta_obj = instagram_parse_json_to_obj(js_str)
    assert (
        insta_obj.video_url
        == "https://scontent-sjc3-1.cdninstagram.com/v/t50.2886-16/205064059_2276556202474871_4228301026603728176_n.mp4?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=111&_nc_ohc=k8l8DhYtjCMAX9C8LNP&edm=APfKNqwBAAAA&ccb=7-4&oe=60E408DE&oh=3ff999247ea45edd802b746e6f0c6e83&_nc_sid=74f7ba"
    )


if __name__ == '__main__':
    test_converter_instagram_画像複数枚()
