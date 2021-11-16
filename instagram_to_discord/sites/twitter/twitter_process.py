
from ...params import IS_DEBUG
from .twitter import send_twitter_images_from_cache_for_specified_index
from ...boto3 import upload_video_file
from ...download import (download_file_to_path, make_twitter_mp4_filename)
from .twitter import (create_new_image_urls_with_downloading, get_twitter_object, twitter_extract_tweet_id,
                      twitter_extract_tweet_url)
from ...const_value import FSIZE_TARGET
import os
import discord
from typing import Any
from logging import getLogger, StreamHandler, INFO
logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


async def process_twitter(client: Any, channel, message, content):
    client.last_url_twitter[channel] = twitter_extract_tweet_url(content)
    client.is_twitter_last = True

    nums = [1]

    tweet_id = twitter_extract_tweet_id(content)
    tw = get_twitter_object(tweet_id)

    # 画像を取得する
    image_urls = tw.image_urls
    # TODO: もしキャッシュが存在していれば(KVS)、ダウンロードしないしアップロードもしない。
    new_image_urls = create_new_image_urls_with_downloading(
        tweet_id, image_urls)

    msg_list = content.split()
    if len(msg_list) > 1:
        nums = msg_list[1].split(",")
        nums = map(lambda x: int(x), nums)
        nums = filter(lambda x: x != 1, nums)
        nums = list(nums)
    elif tw.video_url:
        video_url = tw.video_url.split("?")[0]
        fname_video = make_twitter_mp4_filename(
            "dump_videos", tweet_id, video_url)

        # ファイルダウンロード
        download_file_to_path(video_url, fname_video)

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
                logger.error("[twitter] video: file send error!  : ", e)
                image_urls = tw.image_urls
                await send_twitter_images_from_cache_for_specified_index(
                    skip_one=False,
                    image_urls=image_urls,
                    nums=[1],
                    message=message,
                )  # 動画のサムネイル送信
        if not IS_DEBUG:
            os.remove(fname_video)

    await send_twitter_images_from_cache_for_specified_index(
        skip_one=True, image_urls=new_image_urls, nums=nums, message=message
    )  # 動画のサムネイル送信
