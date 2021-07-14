import os
import discord
from ..youtube import download_youtube_video, extract_youtube_url
from ..boto3 import upload_file
from typing import Dict, Optional

def play_count_to_text(count:int) -> str:
    oku = 0
    man = 0
    res = 0
    if count > 10**8: # 1億を超えてる
        oku = count // 10**8
        count = count % 10**8
    if count > 10 ** 4: # 1万を超えてる
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

def create_youtube_video_embed(base_url: str, info_dict: Dict[str, any], s3_url: Optional[str] = None):
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
        description = s3_url  + "\n"
    else:
        description = ""
    play_count_text = play_count_to_text(info_dict["view_count"])
    uploaded_at_text = uploaded_at_to_text(info_dict["upload_date"])
    description +=  info_dict["description"][:5] # キャプション作りたい
    description += "\n" + f'投稿日: {uploaded_at_text}'
    description += "\n" + f'再生🔁: {play_count_text}'
    description += "\n" + f'時間▶️: {minutes_text}'
    if "like_count" in info_dict:
        description += "\n" + f'👍: {info_dict["like_count"]} 👎: {info_dict["dislike_count"]}'
    embed = discord.Embed(
        title=info_dict["title"],
        description=description,
        url=base_url,
        color=discord.Color.red()
    )

    embed.set_image(url=info_dict["thumbnail"])
    embed.set_author(name=info_dict["channel"],
                    url=info_dict["channel_url"]) # icon_url もある
    return embed

async def handle_youtube_main(client: discord.Client, channel_id:int, content: str):
    await client.wait_until_ready()
    print("[handle_youtube] content: " + content)
    extracted_url: str = extract_youtube_url(content) # is like "https://www.youtube.com/watch?v=Yp6Hc8yN_rs"
    (fname, small_filesize_fname), over_8mb, info_dict = download_youtube_video(extracted_url)

    channel = client.get_channel(id=channel_id) 
    if over_8mb:
        video_s3_url = upload_file(fname)
        embed = create_youtube_video_embed(extracted_url, info_dict, video_s3_url)
        await channel.send(embed=embed)
        await channel.send(file=discord.File(small_filesize_fname))
    else:
        embed = create_youtube_video_embed(extracted_url, info_dict, None)

        await channel.send(embed=embed)
        await channel.send(file=discord.File(fname))

    print("mdmd メッセージ送信終了したので、プロセスexitします: " + info_dict["title"])
    # client.stop()
    # await client.logout()
    await client.close()
    # raise KeyboardInterrupt()


def handle_youtube(channel_id: int,  content: str):
    client = discord.Client()
    TOKEN = os.getenv("TOKEN")
    client.loop.create_task(handle_youtube_main(client, channel_id, content))
    client.run(TOKEN)
