import discord
import os
from debug import DEBUG
from .instagram_type import instagran_parse_json_to_obj, InstagramData, get_multiple_medias_from_str
from .string_util import sophisticate_string
from .converter_instagram_url import instagram_make_author_page, instagram_make_base_url, instagram_extract_from_content
from .converter_instagram_url import convert_instagram_url_to_a
from .cookie_requests import requests_get_cookie
from .twitter_multiple import twitter_line_to_image_urls, twitter_extract_tweet_url, get_twitter_object, twitter_extract_tweet_id
from .util import is_int
from typing import Dict, List
from .download import download_image, make_filename, save_image
from .boto3 import upload_file

class DiscordMessageListener(discord.Client):
    last_url_twitter: Dict[str, str] = {}
    last_url_instagram: Dict[str, str] = {}
    is_twitter_last = True

    def __init__(self):
        super().__init__()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def send_twitter_images_for_specified_index(self, skip_one: bool, image_urls: List[str], nums: List[int], message):
        for n in nums:
            idx = n-1
            assert(idx >= 0)
            assert(idx < 4)
            if len(image_urls) < n:
                continue
            if skip_one and n == 1: continue
            if DEBUG:
                print(f"send_twitter_image: url: {image_urls[idx]}")
            embed = self.create_embed_twitter_image(image_urls[idx])
            await message.channel.send(embed=embed)

    async def send_instagram_images_for_specified_index(self, image_urls: List[str], nums: List[int], message):
        for n in nums:
            idx = n-1
            assert(idx >= 0)
            assert(idx < 4)
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
            color=discord.Color.red()
        )
        embed.set_image(url=obj.media)
        embed.set_author(name=obj.full_name,
                         url=instagram_make_author_page(obj.username),
                         icon_url=obj.profile_url
                         )
        return embed

    async def create_and_send_embed_twitter_video_thumbnail_with_message(self, 
        message,
        thumbnail_image_url:str, 
        s3_video_url: str,
        tweet_url: str,
        author_name: str,
        author_url: str,
        author_profile_image_url: str,
        caption: str
    ):
        description = sophisticate_string(caption)
        embed = discord.Embed(
            title=author_name,
            description=description,
            url=tweet_url,
            color=discord.Color.blue()
        )
        embed.set_image(url=thumbnail_image_url)
        embed.set_author(
                         name=author_name,
                         url=author_url,
                         icon_url=author_profile_image_url
        )
        await message.channel.send(embed=embed)

    def create_embed_twitter_image(self, image_url: str):
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        return embed

    def create_embed_instagram_image(self, image_url: str):
        embed = discord.Embed(
            color=discord.Color.red()
        )
        embed.set_image(url=image_url)
        return embed

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(f"Message from {message.author.display_name}")
        print(f"\tchannel: {message.channel}")
        print(f"\ttype channel: {type(message.channel)}")
        content = message.content
        channel = message.channel

        if "instagram-support" in message.author.display_name: return

        if "https://www.instagram.com/reel/" in content:

        elif "https://www.instagram.com/p/" in content:
            print("[log] channel name: ", message.channel.name)
            extracted_base_url = instagram_extract_from_content(content)
            if not extracted_base_url:
                print("[error] failed to parse base_url for : ", content)
                return
            a_url = convert_instagram_url_to_a(extracted_base_url)
            self.last_url_instagram[channel] = a_url
            self.is_twitter_last = False

            text = requests_get_cookie(url=a_url)
            msg_list = content.split()
            nums = []
            if len(msg_list) > 1:
                nums = msg_list[1].split(",")
                nums = map(lambda x: int(x), nums)
                nums = filter(lambda x: x != 1, nums)
                nums = list(nums)
            else: 
                nums.append(1)

            print("[DEBUG} nums!: ", nums)

            images = get_multiple_medias_from_str(text)

            print("[DEBUG] images: ", images)
            insta_obj = instagran_parse_json_to_obj(text)
            assert(nums[0] >= 1)
            assert(nums[0] <= 4)
            image_url = images[nums[0]-1]
            insta_obj.media = image_url
            embed = self.create_instagram_pic_embed(insta_obj, extracted_base_url)
            await message.channel.send(embed=embed)
            if len(nums) == 1: return
            await self.send_instagram_images_for_specified_index(images, nums[1:], message)

        elif ("https://twitter.com/" in content and "/status/" in content):
            # ここで最後のtwitter url を記録しておく。
            self.last_url_twitter[channel] = twitter_extract_tweet_url(content)
            self.is_twitter_last = True

            nums = [1]  

            tweet_id = twitter_extract_tweet_id(content)
            tw = get_twitter_object(tweet_id)
            print(tw)
            msg_list = content.split()
            if len(msg_list) > 1:
                nums = msg_list[1].split(",")
                nums = map(lambda x: int(x), nums)
                nums = filter(lambda x: x != 1, nums)
                nums = list(nums)
            else:
                # video かどうかを判定する
                # video のサムネでもいい

                if tw.video_url:
                    video_url = tw.video_url.split("?")[0]
                    fname_video = make_filename("", tweet_id, video_url)

                    video = download_image(video_url)
                    # ファイルダウンロード
                    save_image(fname_video, video)

                    # ファイル送信
                    fsize = os.path.getsize(fname_video)
                    print("file size: ", fsize)
                    if fsize > (2**20 * 8):
                        print("inner fsize is larger!: than ", 2**20 * 8)
                        image_urls = tw.image_urls

                        video_s3_url = upload_file(fname_video)
                        await self.create_and_send_embed_twitter_video_thumbnail_with_message(
                            message=message,
                            thumbnail_image_url=image_urls[0],
                            tweet_url=twitter_extract_tweet_url(content),
                            s3_video_url=video_s3_url,
                            author_name=tw.user_display_name,
                            author_url=tw.user_url,
                            author_profile_image_url=tw.user_profile_image_url,
                            caption= f"{video_s3_url}\n{tw.text}" 
                        )
                        # await self.send_twitter_images_for_specified_index(skip_one = False, image_urls = image_urls, nums = [1], message = message) # 動画のサムネイル送信
                        print("[fsize] image urls: ", image_urls)
                    else:
                        try:
                            await message.channel.send(file=discord.File(fname_video))
                        except Exception as e:
                            print("file send error!  : ",  e)
                            image_urls = tw.image_urls
                            await self.send_twitter_images_for_specified_index(skip_one = False, image_urls = image_urls, nums = [1], message = message) # 動画のサムネイル送信
                            print("image urls: ", image_urls)
                    os.remove(fname_video)

            # 画像を取得する
            image_urls = tw.image_urls
            print("image_urls: ", image_urls)
            await self.send_twitter_images_for_specified_index(skip_one = True, image_urls = image_urls, nums = nums, message = message) # 動画のサムネイル送信
 
        elif len(list(filter(lambda x: is_int(x), content.split(",")))) > 0 and \
               ( channel in self.last_url_twitter or channel in self.last_url_instagram ): # last_url_twitter が存在する。
            if self.is_twitter_last:
                nums = list(map(lambda x: int(x), filter(lambda x: is_int(x), content.split(","))))
                image_urls = twitter_line_to_image_urls(self.last_url_twitter[channel])
                await self.send_twitter_images_for_specified_index(skip_one = True, image_urls = image_urls, nums = nums, message = message) # 動画のサムネイル送信
            else:
                nums = list(map(lambda x: int(x), filter(lambda x: is_int(x), content.split(","))))
                text = requests_get_cookie(url=self.last_url_instagram[channel])
                image_urls = get_multiple_medias_from_str(text)
                await self.send_twitter_images_for_specified_index(skip_one = True, image_urls = image_urls, nums = nums, message = message) # 動画のサムネイル送信

def main():
    client = DiscordMessageListener()

    TOKEN = os.getenv("TOKEN")
    if DEBUG and TOKEN:
        print("TOKEN: ", TOKEN[0:4] + "....." + TOKEN[-3:])
    client.run(TOKEN)
