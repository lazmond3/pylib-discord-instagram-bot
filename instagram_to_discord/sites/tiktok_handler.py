import os
import re
from typing import Any, Dict, Optional

import discord

from ..boto3 import upload_file
from ..tiktok import download_tiktok_video, extract_tiktok_url
from ..video import trimming_video_to_8MB


def play_count_to_text(count: int) -> str:
    oku = 0
    man = 0
    res = 0
    if count > 10 ** 8:  # 1億を超えてる
        oku = count // 10 ** 8
        count = count % 10 ** 8
    if count > 10 ** 4:  # 1万を超えてる
        man = count // 10 ** 4
        count = count % 10 ** 4
    res = count

    ans = ""
    if oku > 0:
        ans += f"{oku}億"
    if man > 0:
        ans += f"{man}万"
    ans += f"{res}回"
    return ans


def uploaded_at_to_text(datest: str) -> str:
    year = datest[:4]
    month = datest[4:6]
    day = datest[6:]
    return f"{year}年{month}月{day}日"


def convert_to_author_url(webpage_url: str) -> str:
    m = re.match(r"(https://(www.)?tiktok.com/@[^/]+)", webpage_url)
    if m:
        return m.group(1)
    raise Exception("[tiktok convert_to_author_url] 変換できません: " + webpage_url)


def create_tiktok_video_embed(info_dict: Dict[str, Any], s3_url: Optional[str] = None):
    seconds = info_dict["duration"]
    minutes = None
    if seconds > 60:
        minutes = seconds // 60
        seconds = seconds % 60
    minutes_text = ""
    if minutes:
        minutes_text += f"{minutes:}分"
    minutes_text += f"{seconds:02}秒"

    if s3_url:
        description = s3_url + "\n"
    else:
        description = ""
    play_count_text = play_count_to_text(info_dict["view_count"])
    uploaded_at_text = uploaded_at_to_text(info_dict["upload_date"])
    description += "\n".join(info_dict["description"].split("\n")[:5])  # キャプション作りたい
    description += "\n" + f"投稿日: {uploaded_at_text}"
    description += "\n" + f"再生🔁: {play_count_text}"
    description += "\n" + f"時間▶️: {minutes_text}"
    if "like_count" in info_dict:
        description += "\n" + f'👍: {info_dict["like_count"]}'

    author_url = convert_to_author_url(info_dict["webpage_url"])
    embed = discord.Embed(
        title=info_dict["title"],
        description=description,
        url=info_dict["webpage_url"],
        color=discord.Color(0x3A3939),  # 黒
    )

    embed.set_image(url=info_dict["thumbnail"])
    embed.set_author(name=info_dict["uploader"], url=author_url)
    return embed


async def handle_tiktok_main(client: discord.Client, channel_id: int, content: str):
    await client.wait_until_ready()
    extracted_url: str = extract_tiktok_url(
        content
    )  # is like "https://www.youtube.com/watch?v=Yp6Hc8yN_rs"
    fname, over_8mb, info_dict = download_tiktok_video(extracted_url)

    channel = client.get_channel(id=channel_id)
    if over_8mb:
        video_s3_url = upload_file(fname)
        embed = create_tiktok_video_embed(info_dict, video_s3_url)
        small_filesize_fname = trimming_video_to_8MB(fname)
        await channel.send(embed=embed)
        await channel.send(file=discord.File(small_filesize_fname))
    else:
        embed = create_tiktok_video_embed(info_dict, None)

        await channel.send(embed=embed)
        await channel.send(file=discord.File(fname))

    print("[handle_tiktok_main] メッセージ送信終了したので、プロセスexitします: " + info_dict["title"])
    # await client.close()


def handle_tiktok(channel_id: int, content: str):
    client = discord.Client()
    TOKEN = os.getenv("TOKEN")
    client.loop.create_task(handle_tiktok_main(client, channel_id, content))
    client.run(TOKEN)
