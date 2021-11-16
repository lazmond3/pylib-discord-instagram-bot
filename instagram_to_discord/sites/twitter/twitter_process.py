from typing import Any
import discord
import os
from ...const_value import FSIZE_TARGET
from ...twitter_multiple import (get_twitter_object, twitter_extract_tweet_id,
                                 twitter_extract_tweet_url)
from ...download import (download_file, make_twitter_image_filename,
                         make_twitter_mp4_filename, save_image)
from ...boto3 import upload_video_file, upload_image_file
from .twitter import send_twitter_images_from_cache_for_specified_index


async def process_twitter(client: Any, channel, message, content):
    client.last_url_twitter[channel] = twitter_extract_tweet_url(content)
    client.is_twitter_last = True

    nums = [1]

    tweet_id = twitter_extract_tweet_id(content)
    tw = get_twitter_object(tweet_id)
    msg_list = content.split()
    if len(msg_list) > 1:
        nums = msg_list[1].split(",")
        nums = map(lambda x: int(x), nums)
        nums = filter(lambda x: x != 1, nums)
        nums = list(nums)
    elif tw.video_url:
        video_url = tw.video_url.split("?")[0]
        fname_video = make_twitter_mp4_filename("", tweet_id, video_url)

        video = download_file(video_url)
        # ファイルダウンロード
        save_image(fname_video, video)

        # ファイル送信
        fsize = os.path.getsize(fname_video)
        if fsize > (FSIZE_TARGET):

            image_urls = tw.image_urls

            video_s3_url = upload_video_file(fname_video)
            await message.channel.send(video_s3_url)

        else:
            try:
                await message.channel.send(file=discord.File(fname_video))
            except Exception as e:
                print("file send error!  : ", e)
                image_urls = tw.image_urls
                await send_twitter_images_from_cache_for_specified_index(
                    skip_one=False,
                    image_urls=image_urls,
                    nums=[1],
                    message=message,
                )  # 動画のサムネイル送信
        os.remove(fname_video)

    # 画像を取得する
    image_urls = tw.image_urls
    new_image_urls = []
    for idx, u in enumerate(image_urls):
        idx += 1
        fname_image = make_twitter_image_filename("", tweet_id, idx, u)
        image_data = download_file(u)
        # ファイルダウンロード
        save_image(fname_image, image_data)
        path = upload_image_file(fname_image, tweet_id, idx)
        new_image_urls.append(path)
        # os.remove(fname_image)

    await send_twitter_images_from_cache_for_specified_index(
        skip_one=True, image_urls=new_image_urls, nums=nums, message=message
    )  # 動画のサムネイル送信
