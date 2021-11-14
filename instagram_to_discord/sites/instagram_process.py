from typing import Any
import discord
import os
from ..const_value import FSIZE_TARGET
from ..twitter_multiple import (get_twitter_object, twitter_extract_tweet_id,
                               twitter_extract_tweet_url,
                               twitter_line_to_image_urls)
from ..download import (download_file, make_instagram_mp4_filename, make_twitter_image_filename,
                       make_twitter_mp4_filename, save_image)
from ..boto3 import upload_video_file, upload_image_file
from .twitter import send_twitter_images_for_specified_index

from ..converter_instagram_url import (convert_instagram_url_to_a,
                                      instagram_extract_from_content,
                                      instagram_make_author_page)
from ..cookie_requests import requests_get_cookie
from ..instagram_type import (InstagramData, get_multiple_medias_from_str,
                             instagran_parse_json_to_obj)
from .instagram import send_instagram_images_for_specified_index, create_instagram_pic_embed, create_instagram_video_embed
from ..video import trimming_video_to_8MB

async def process_instagram(client: Any, channel, message, content):
    print("[log] channel name: ", message.channel.name)
    extracted_base_url = instagram_extract_from_content(content)
    if not extracted_base_url:
        print("[error] failed to parse base_url for : ", content)
        return
    a_url = convert_instagram_url_to_a(extracted_base_url)
    client.last_url_instagram[channel] = a_url
    client.is_twitter_last = False

    text = requests_get_cookie(url=a_url)
    insta_obj = instagran_parse_json_to_obj(text)
    if insta_obj.is_video:
        video_url = insta_obj.video_url

        fname_video = make_instagram_mp4_filename("", video_url)
        video_content = download_file(video_url)
        save_image(fname_video, video_content)
        fsize = os.path.getsize(fname_video)
        if fsize > FSIZE_TARGET:
            print("[insta-video] inner fsize is larger!: than ", FSIZE_TARGET)

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
                print("[instagram video upload] file send error!  : ", e)
        os.remove(fname_video)
    else:
        images = get_multiple_medias_from_str(text)

        for image in images:
            print("[listener][twitter] image: " + image)
        insta_obj = instagran_parse_json_to_obj(text)

        msg_list = content.split()
        nums = []
        if len(msg_list) > 1:
            nums = msg_list[1].split(",")
            nums = map(lambda x: int(x), nums)
            nums = list(nums)
        else:
            nums.append(1)
        assert nums[0] >= 1

        image_url = images[nums[0] - 1]
        insta_obj.media = image_url
        embed = create_instagram_pic_embed(insta_obj, extracted_base_url)
        await message.channel.send(embed=embed)
        if len(nums) == 1:
            return
        await send_instagram_images_for_specified_index(
            images, nums[1:], message
        )