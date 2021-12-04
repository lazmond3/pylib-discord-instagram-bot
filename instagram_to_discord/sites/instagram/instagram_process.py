from ...video import trimming_video_to_8MB
from .instagram_sender import get_instagram_id_from_url, send_instagram_images_for_specified_index
from .instagram_type import (get_multiple_medias_from_str, get_multiple_mediasV2_from_str,
                             instagram_parse_json_to_obj)
from ...cookie_requests import requests_get_cookie
from .converter_instagram_url import (convert_instagram_url_to_a,
                                      instagram_extract_from_content)
from ...boto3 import add_instagram_json_to_dynamo_instagram_json, upload_video_file, upload_image_file
from ...download import (download_file, make_instagram_image_filename,
                         make_instagram_mp4_filename, save_image)
from ...const_value import FSIZE_TARGET
import os
import json
import discord
from typing import Any
from ...const_value import IS_DEBUG
from logging import getLogger, StreamHandler, INFO, DEBUG

from instagram_to_discord.util2.embed import create_instagram_pic_embed, create_instagram_video_embed
logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

if IS_DEBUG:
    logger.setLevel(DEBUG)


async def process_instagram(client: Any, channel, message, content):
    logger.debug("[log] channel name: ", message.channel.name)
    extracted_base_url = instagram_extract_from_content(content)
    if not extracted_base_url:
        logger.error("[error] failed to parse base_url for : ", content)
        return
    a_url = convert_instagram_url_to_a(extracted_base_url)
    client.last_url_instagram[channel] = a_url
    client.is_twitter_last = False

    text = requests_get_cookie(url=a_url)
    instagram_id = ""
    if "/p/" in a_url:
        instagram_id = a_url.split("/p/")[1].split("/")[0]
    elif "/reel/" in a_url:
        instagram_id = a_url.split("/reel/")[1].split("/")[0]
    # TODO: stories に対応できるようにする。
    js = json.loads(text)
    with open(f"dump_json_instagram/dump_instagram_{instagram_id}.json", "w") as f:
        json.dump(js, f, ensure_ascii=False)

    # unicode escape
    with open(f"dump_json_instagram/dump_instagram_{instagram_id}.json") as f:
        text_decoded = f.read()
    add_instagram_json_to_dynamo_instagram_json(
        a_url, instagram_id, text_decoded)

    insta_obj = instagram_parse_json_to_obj(text)
    images = get_multiple_medias_from_str(text)
    medias = get_multiple_mediasV2_from_str(text)

    instagram_id = get_instagram_id_from_url(a_url)
    new_uploaded_media_urls = []

    # TODO:
    # もし instagram_id に対して、データを保存済みだったら、これを行わない (cdn でも、BANが怖い) 遅いため
    # dynamo DB に cache を 用意する。
    # IS_FORCE_DOWNLOAD だったら、これを行う、とかにする。
    # コマンドラインツールにすれば ？
    for idx, me in enumerate(medias):
        logger.debug(
            "[listener][instagram] download image local and upload to s3: image: " + me.url)
        idx += 1
        fname_media = make_instagram_image_filename(
            "",
            instagram_id,
            idx,
            me.url,
        )
        image_data = download_file(me.url)
        # ファイルダウンロード
        save_image(fname_media, image_data)
        path = upload_image_file(fname_media, instagram_id, idx)

        new_uploaded_media_urls.append(path)
        os.remove(fname_media)

    # TODO: 1枚だけvideo, 他は画像のケースに対応できるようにする。
    if insta_obj.is_video:
        video_url = insta_obj.video_url

        fname_video = make_instagram_mp4_filename(
            "dump_videos_instagram", video_url)
        video_content = download_file(video_url)
        save_image(fname_video, video_content)
        fsize = os.path.getsize(fname_video)
        if fsize > FSIZE_TARGET:
            logger.info(
                "[insta-video] inner fsize is larger!: than ", FSIZE_TARGET)

            video_s3_url = upload_video_file(fname_video)
            insta_obj.caption = video_s3_url + "\n" + insta_obj.caption
            embed = create_instagram_pic_embed(
                insta_obj, extracted_base_url
            )
            new_fname_small_video = trimming_video_to_8MB(fname_video)
            await message.channel.send(embed=embed)
            await message.channel.send(file=discord.File(new_fname_small_video))
        else:
            # サムネ 1枚 + ファイルアップロード
            try:
                embed = create_instagram_video_embed(
                    insta_obj, extracted_base_url
                )
                await message.channel.send(embed=embed)
                await message.channel.send(file=discord.File(fname_video))
            except Exception as e:
                logger.error(
                    "[instagram video upload] file send error!  : ", e)
        if not IS_DEBUG:
            os.remove(fname_video)
    else:
        insta_obj = instagram_parse_json_to_obj(text)

        msg_list = content.split()
        nums = []
        try:
            if len(msg_list) > 1:
                nums = msg_list[1].split(",")
                nums = map(lambda x: int(x), nums)
                nums = list(nums)
            else:
                nums.append(1)
        except ValueError:
            logger.info(
                f"[instagram_process] 文字付き: ツイートの後の文字が数字じゃなかった: {msg_list[1]}")
            nums = [1]

        assert nums[0] >= 1

        media_url = new_uploaded_media_urls[nums[0] - 1]
        insta_obj.media = media_url  # TODO: video URL が入るかもしれないので気持ち悪いが...?

        embed = create_instagram_pic_embed(insta_obj, extracted_base_url)
        await message.channel.send(embed=embed)

        if len(nums) == 1:
            return
        await send_instagram_images_for_specified_index(
            new_uploaded_media_urls, nums[1:], message
        )
