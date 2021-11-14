import os
from typing import Dict, List

import discord
from debug import DEBUG

from .boto3 import upload_file, upload_image_file
from .const_value import FSIZE_TARGET
from .converter_instagram_url import (convert_instagram_url_to_a,
                                      instagram_extract_from_content,
                                      instagram_make_author_page)
from .cookie_requests import requests_get_cookie
from .download import (download_file, make_instagram_mp4_filename, make_twitter_image_filename,
                       make_twitter_mp4_filename, save_image)
from .instagram_type import (InstagramData, get_multiple_medias_from_str,
                             instagran_parse_json_to_obj)
from .sites.tiktok_handler import handle_tiktok_main
from .sites.youtube_handler import handle_youtube_main
from .string_util import sophisticate_string
from .twitter_multiple import (get_twitter_object, twitter_extract_tweet_id,
                               twitter_extract_tweet_url,
                               twitter_line_to_image_urls)
from .util import is_int
from .video import trimming_video_to_8MB

IS_DEBUG = os.getenv("IS_DEBUG")

class DiscordMessageListener(discord.Client):
    last_url_twitter: Dict[str, str] = {}
    last_url_instagram: Dict[str, str] = {}
    is_twitter_last = True

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def send_twitter_images_for_specified_index(
        self, skip_one: bool, image_urls: List[str], nums: List[int], message
    ):
        for n in nums:
            idx = n - 1
            assert idx >= 0
            assert idx < 4
            if len(image_urls) < n:
                continue
            if skip_one and n == 1:
                continue
            if DEBUG:
                print(f"send_twitter_image: url: {image_urls[idx]}")
            embed = self.create_embed_twitter_image(image_urls[idx])
            await message.channel.send(embed=embed)

    async def send_instagram_images_for_specified_index(
        self, image_urls: List[str], nums: List[int], message
    ):
        for n in nums:
            idx = n - 1
            assert idx >= 0
            if len(image_urls) < n:
                continue
            # if n == 1: continue
            if DEBUG:
                print(f"send_twitter_image: url: {image_urls[idx]}")
            embed = self.create_embed_instagram_image(image_urls[idx])
            await message.channel.send(embed=embed)

    def create_instagram_pic_embed(self, obj: InstagramData, base_url: str):
        description = sophisticate_string(obj.caption)
        embed = discord.Embed(
            title=obj.full_name,
            description=description,
            url=base_url,
            color=discord.Color.red(),
        )
        embed.set_image(url=obj.media)
        embed.set_author(
            name=obj.full_name,
            url=instagram_make_author_page(obj.username),
            icon_url=obj.profile_url,
        )
        return embed

    def create_instagram_video_embed(self, obj: InstagramData, base_url: str):
        description = sophisticate_string(obj.caption)
        embed = discord.Embed(
            title=obj.full_name,
            description=description,
            url=base_url,
            color=discord.Color.red(),
        )
        # embed.set_image(url=obj.media)
        embed.set_author(
            name=obj.full_name,
            url=instagram_make_author_page(obj.username),
            icon_url=obj.profile_url,
        )
        return embed

    async def create_and_send_embed_twitter_video_thumbnail_with_message(
        self,
        message,
        thumbnail_image_url: str,
        s3_video_url: str,
        tweet_url: str,
        author_name: str,
        author_url: str,
        author_profile_image_url: str,
        caption: str,
    ):
        description = sophisticate_string(caption)
        embed = discord.Embed(
            title=author_name,
            description=description,
            url=tweet_url,
            color=discord.Color.blue(),
        )
        embed.set_image(url=thumbnail_image_url)
        embed.set_author(
            name=author_name, url=author_url, icon_url=author_profile_image_url
        )
        await message.channel.send(embed=embed)

    def create_embed_twitter_image(self, image_url: str):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=image_url)
        return embed

    def create_embed_instagram_image(self, image_url: str):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_image(url=image_url)
        return embed

    async def on_message(self, message):
        print(
            "Message from {0.author.display_name} in ({0.channel}): {0.content}".format(
                message
            )
        )
        content = message.content
        channel = message.channel
        if IS_DEBUG and "debug" not in channel.name: return


        if "instagram-support" in message.author.display_name:
            return

        if (
            "https://www.youtube.com" in content
            or "https://youtu.be" in content
            or "https://youtube.com" in content
        ):

            print("[youtube] channel: ", channel.id)

            await handle_youtube_main(self, channel_id=channel.id, content=content)
            # p = Process(target=handle_youtube, args=(channel.id, content))
            # p.start()

        elif "https://" in content and "tiktok.com" in content:
            print("[tiktok] -> " + content, channel.id)
            await handle_tiktok_main(self, channel_id=channel.id, content=content)
            # p = Process(target=handle_tiktok, args=(channel.id, content))
            # p.start()

        elif "https://www.instagram.com/" in content and (
            "/p/" in content or "/reel/" in content
        ):
            print("[log] channel name: ", message.channel.name)
            extracted_base_url = instagram_extract_from_content(content)
            if not extracted_base_url:
                print("[error] failed to parse base_url for : ", content)
                return
            a_url = convert_instagram_url_to_a(extracted_base_url)
            self.last_url_instagram[channel] = a_url
            self.is_twitter_last = False

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

                    video_s3_url = upload_file(fname_video)
                    insta_obj.caption = video_s3_url + "\n" + insta_obj.caption
                    embed = self.create_instagram_pic_embed(
                        insta_obj, extracted_base_url
                    )
                    new_fname_small_video = trimming_video_to_8MB(fname_video)
                    await message.channel.send(embed=embed)
                    await message.channel.send(file=discord.File(new_fname_small_video))
                else:
                    # サムネ 1枚 + ファイルアップロード
                    try:
                        embed = self.create_instagram_video_embed(
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
                embed = self.create_instagram_pic_embed(insta_obj, extracted_base_url)
                await message.channel.send(embed=embed)
                if len(nums) == 1:
                    return
                await self.send_instagram_images_for_specified_index(
                    images, nums[1:], message
                )

        elif "https://twitter.com/" in content and "/status/" in content:
            # ここで最後のtwitter url を記録しておく。
            self.last_url_twitter[channel] = twitter_extract_tweet_url(content)
            self.is_twitter_last = True

            nums = [1]

            tweet_id = twitter_extract_tweet_id(content)
            tw = get_twitter_object(tweet_id)
            msg_list = content.split()
            if len(msg_list) > 1:
                nums = msg_list[1].split(",")
                nums = map(lambda x: int(x), nums)
                nums = filter(lambda x: x != 1, nums)
                nums = list(nums)
            else:
                if tw.video_url:
                    video_url = tw.video_url.split("?")[0]
                    fname_video = make_twitter_mp4_filename("", tweet_id, video_url)

                    video = download_file(video_url)
                    # ファイルダウンロード
                    save_image(fname_video, video)

                    # ファイル送信
                    fsize = os.path.getsize(fname_video)
                    if fsize > (FSIZE_TARGET):

                        image_urls = tw.image_urls

                        video_s3_url = upload_file(fname_video)
                        await message.channel.send(video_s3_url)

                        # twitter は、そもそも OGPがあるので、 動画の時のembed は不要
                        # mp4のURL貼るとそれがサムネに表示される。ので、トリミングした動画投稿も不要

                        # await self.create_and_send_embed_twitter_video_thumbnail_with_message(
                        #     message=message,
                        #     thumbnail_image_url=image_urls[0],
                        #     tweet_url=twitter_extract_tweet_url(content),
                        #     s3_video_url=video_s3_url,
                        #     author_name=tw.user_display_name,
                        #     author_url=tw.user_url,
                        #     author_profile_image_url=tw.user_profile_image_url,
                        #     caption= f"{video_s3_url}\n{tw.text}"
                        # )

                        # 8MB 以上なので削る
                        # new_fname_small_video = trimming_video_to_8MB(fname_video)
                        # await message.channel.send(file=discord.File(new_fname_small_video))
                    else:
                        try:
                            await message.channel.send(file=discord.File(fname_video))
                        except Exception as e:
                            print("file send error!  : ", e)
                            image_urls = tw.image_urls
                            await self.send_twitter_images_for_specified_index(
                                skip_one=False,
                                image_urls=image_urls,
                                nums=[1],
                                message=message,
                            )  # 動画のサムネイル送信
                    os.remove(fname_video)

            # 画像を取得する
            image_urls = tw.image_urls
            for idx,u in enumerate(image_urls):
                fname_image = make_twitter_image_filename("", tweet_id, idx,u )
                image_data = download_file(u)
                # ファイルダウンロード
                save_image(fname_image, image_data)
                upload_image_file(fname_image, tweet_id, idx)
                os.remove(fname_image)


            await self.send_twitter_images_for_specified_index(
                skip_one=True, image_urls=image_urls, nums=nums, message=message
            )  # 動画のサムネイル送信

        elif len(list(filter(lambda x: is_int(x), content.split(",")))) > 0 and (
            channel in self.last_url_twitter or channel in self.last_url_instagram
        ):  # last_url_twitter が存在する。
            if self.is_twitter_last:
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                image_urls = twitter_line_to_image_urls(self.last_url_twitter[channel])
                await self.send_twitter_images_for_specified_index(
                    skip_one=True, image_urls=image_urls, nums=nums, message=message
                )  # 動画のサムネイル送信
            else:  # instagram
                nums = list(
                    map(
                        lambda x: int(x),
                        filter(lambda x: is_int(x), content.split(",")),
                    )
                )
                text = requests_get_cookie(url=self.last_url_instagram[channel])
                image_urls = get_multiple_medias_from_str(text)
                await self.send_twitter_images_for_specified_index(
                    skip_one=False, image_urls=image_urls, nums=nums, message=message
                )  # 動画のサムネイル送信


def main():
    client = DiscordMessageListener()

    TOKEN = os.getenv("TOKEN")
    if DEBUG and TOKEN:
        print("TOKEN: ", TOKEN[0:4] + "....." + TOKEN[-3:])
    client.run(TOKEN)
