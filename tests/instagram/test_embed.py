
import discord
from instagram_to_discord.sites.instagram.converter_instagram_url import instagram_make_author_page
from instagram_to_discord.sites.instagram.instagram_type import instagram_parse_json_to_obj, instagram_parse_json_to_obj_v2
from instagram_to_discord.string_util import sophisticate_string
from instagram_to_discord.util2.embed import create_instagram_pic_embed, create_instagram_video_embed


def test_embed_from_json_text():
    # mocker.patch.object(instagram_to_discord.sites.instagram.instagram_process, "instagram_parse_json_to_obj", return_value=insta_obj)  # nopep8
    text = ""
    with open("tests/data/dump_instagram_CW4YfYIvgHD.json") as f:
        text = f.read()

    insta_obj = instagram_parse_json_to_obj(text)
    extracted_base_url = "https://www.instagram.com/p/CW4YfYIvgHD"
    insta_obj.media = "https://discord-python-image.s3.ap-northeast-1.amazonaws.com/CW4YfYIvgHD/5.jpg"

    target_embed = create_instagram_pic_embed(
        insta_obj, extracted_base_url
    )

    answer_embed = discord.Embed(
        title="佐々木希",
        description=sophisticate_string("#VOCE 2022年1月号 \nオフショット💄💕"),
        url="https://www.instagram.com/p/CW4YfYIvgHD",
        color=discord.Color.red(),
    )
    answer_embed.set_image(  # 5 の場合
        url="https://discord-python-image.s3.ap-northeast-1.amazonaws.com/CW4YfYIvgHD/5.jpg")
    answer_embed.set_author(
        name="佐々木希",
        url=instagram_make_author_page("nozomisasaki_official"),
        icon_url="https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/24175048_1706810412710767_1281070886199230464_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=OzlpjF-F5_MAX_zYlhx&edm=AABBvjUBAAAA&ccb=7-4&oh=6954b174179012577379e144883a0456&oe=61B40F0F&_nc_sid=83d603"
    )

    assert target_embed.title == answer_embed.title
    assert target_embed.description == answer_embed.description
    assert target_embed.url == answer_embed.url
    assert target_embed.color == answer_embed.color
    assert target_embed._author == answer_embed._author
    assert target_embed._image == answer_embed._image

def test_new_shigeta_multiple_images_embed_from_json_text():
    # mocker.patch.object(instagram_to_discord.sites.instagram.instagram_process, "instagram_parse_json_to_obj", return_value=insta_obj)  # nopep8
    text = ""
    with open("tests/data/instagram_multiple_image_and_video_new_佐々木.json") as f:
        text = f.read()

    insta_obj = instagram_parse_json_to_obj_v2(text)
    extracted_base_url = "https://www.instagram.com/p/CW4YfYIvgHD"
    insta_obj.media = "https://discord-python-image.s3.ap-northeast-1.amazonaws.com/CW4YfYIvgHD/5.jpg"

    target_embed = create_instagram_pic_embed(
        insta_obj, extracted_base_url
    )

    answer_embed = discord.Embed(
        title="佐々木希",
        description=sophisticate_string("#VOCE 2022年1月号 \nオフショット💄💕"),
        url="https://www.instagram.com/p/CW4YfYIvgHD",
        color=discord.Color.red(),
    )
    answer_embed.set_image(  # 5 の場合
        url="https://discord-python-image.s3.ap-northeast-1.amazonaws.com/CW4YfYIvgHD/5.jpg")
    answer_embed.set_author(
        name="佐々木希",
        url=instagram_make_author_page("nozomisasaki_official"),
        icon_url="https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/s150x150/24175048_1706810412710767_1281070886199230464_n.jpg?_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=1&_nc_ohc=GFwOPq7_OSoAX9Z7mXX&edm=AABBvjUBAAAA&ccb=7-4&oh=00_AT9lIjlLHKkk0nDijbKcw1CjoslGzW-cNELygz1nwCUJeg&oe=61F74B8F&_nc_sid=83d603"
    )

    assert target_embed.title == answer_embed.title
    assert target_embed.description == answer_embed.description
    assert target_embed.url == answer_embed.url
    assert target_embed.color == answer_embed.color
    assert target_embed._author == answer_embed._author
    assert target_embed._image == answer_embed._image
