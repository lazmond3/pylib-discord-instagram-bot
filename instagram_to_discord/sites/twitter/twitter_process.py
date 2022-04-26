import os
from logging import INFO, StreamHandler, getLogger

import discord

from instagram_to_discord.sites.ask.ask import (
    get_ask_html_text_from_url, process_question_and_answer_from_text)
from instagram_to_discord.util2.embed import (create_ask_embed,
                                              create_twitter_description_image)
from instagram_to_discord.util2.types import DiscordMemoClient

from ...boto3 import upload_video_file
from ...const_value import IS_DEBUG
from ...download import download_file_to_path, make_twitter_mp4_filename
from .twitter import (create_new_image_urls_with_downloading,
                      get_twitter_object,
                      send_twitter_images_from_cache_for_specified_index,
                      twitter_extract_tweet_id, twitter_extract_tweet_url)

logger = getLogger(__name__)  # 以降、このファイルでログが出たということがはっきりする。
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


async def process_twitter_open(message: discord.Message, twitter_url: str):
    tweet_id = twitter_extract_tweet_id(twitter_url)
    tw = get_twitter_object(tweet_id)
    image_urls = tw.image_urls
    new_image_urls = create_new_image_urls_with_downloading(tweet_id, image_urls)
    image_url = None
    if len(image_urls) > 0:
        image_url = new_image_urls[0]
    embed = create_twitter_description_image(tw, image_url=image_url)
    await message.channel.send(embed=embed)


async def process_twitter(
    client: DiscordMemoClient, message: discord.Message, content: str
):
    channel: discord.TextChannel = message.channel
    print(f"channel : {channel}, mes: {message}")
    client.last_url_twitter[channel] = twitter_extract_tweet_url(content)
    client.is_twitter_last = True

    nums = [1]

    tweet_id = twitter_extract_tweet_id(content)
    tw = get_twitter_object(tweet_id)

    logger.debug(f"tw author: {tw.user_screen_name} tx: {tw.text} link: {tw.link}")
    # tw author: koba31okm tx: 兄弟と現在仲良いですか？？今大学生なんですけど、打算的に見える兄が少し嫌いです。 — 私は現在は仲良くやってますし、そうなって良かったと思ってます。子供ができたときに、親兄弟と仲が悪いのってあまり胸張って子供に言えることじゃないし、今どきは子供がお友達と… https://t.co/sM2nxsgWzb
    if tw.user_screen_name == "koba31okm" and "ask.fm" in tw.link:
        ask_html_text = get_ask_html_text_from_url(tw.link)
        ask_q, ask_a = process_question_and_answer_from_text(ask_html_text)
        embed = create_ask_embed(ask_q, ask_a, tw.link)
        await message.channel.send(embed=embed)

    # 画像を取得する
    # TODO: これ使ってないのでは？
    image_urls = tw.image_urls
    # TODO: もしキャッシュが存在していれば(KVS)、ダウンロードしないしアップロードもしない。
    new_image_urls = create_new_image_urls_with_downloading(tweet_id, image_urls)

    msg_list = content.split()

    if tw.video_url:
        video_url = tw.video_url.split("?")[0]
        fname_video = make_twitter_mp4_filename("dump_videos", tweet_id, video_url)

        # ファイルダウンロード
        download_file_to_path(video_url, fname_video)

        # ファイル送信
        # fsize = os.path.getsize(fname_video)
        # if fsize > (FSIZE_TARGET):

        image_urls = tw.image_urls

        video_s3_url = upload_video_file(fname_video)
        await message.channel.send(video_s3_url)
        if not IS_DEBUG:
            os.remove(fname_video)

    elif len(msg_list) > 1:

        if msg_list[1] == "o":
            await process_twitter_open(
                message=message, twitter_url=client.last_url_twitter[channel]
            )

        nums = msg_list[1].split(",")
        try:
            nums = map(lambda x: int(x), nums)
            # nums = filter(lambda x: x != 1, nums)
            nums = list(nums)
        except ValueError:
            logger.info(f"\t[tweet_process] 文字付き: ツイート後の文字が数字じゃなかった： {msg_list[1]}")
            return

    await send_twitter_images_from_cache_for_specified_index(
        skip_one=True, image_urls=new_image_urls, nums=nums, message=message
    )  # 動画のサムネイル送信
