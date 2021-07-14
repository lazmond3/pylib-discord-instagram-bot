import youtube_dl
import os
import json
import re
# import ffmpeg
import subprocess
from typing import Tuple, Dict
from . import FSIZE_TARGET
from .video import trimming_video_to_8MB

# https://vt.tiktok.com/ZSJgGCR9S/
# https://www.tiktok.com/@kaneko_miyu/video/6971365250369064194?_d=secCgYIASAHKAESMgowAnrkilibsXu8OHJHI0tnKpfT4pH582RdUcNXmvEpD3JsVw%2Bsbb1JFy9hU7%2BFnhceGgA%3D&language=ja&mid=6934737096636730113&preview_pb=0&region=JP&share_app_id=1180&share_item_id=6971365250369064194&share_link_id=1943A867-43D2-42BE-A423-D2B4681A65B3&source=h5_t&timestamp=1626256671&tt_from=copy&u_code=0&utm_campaign=client_share&utm_medium=ios&utm_source=copy&_r=1&is_copy_url=1&is_from_webapp=v1
def extract_tiktok_url(text:str) -> str:
    m = re.match(r".*(https://(www.)?(vt.)?tiktok.com/[^&]+)&?.*", text)
    if m:
        url = m.group(1)
        return url

    raise Exception("[extract_tiktok_url] failed for text: " + text)

def download_tiktok_video(url: str) -> Tuple[Tuple[str], bool, Dict[str, any]]:
    ydlmp4 = youtube_dl.YoutubeDL(
        {
            'outtmpl': "%(id)s" + '.mp4',
            'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'format': "0",
        })
    info_dict = ydlmp4.extract_info(url, download=True)
    with open("dump_" + info_dict["id"] + ".json", "w") as f:
        import json
        json.dump(info_dict, f, ensure_ascii=False)
    old_fname = info_dict["id"] + ".mp4"
    replaced_title = info_dict["title"].replace(" ", "_").replace("　", "__").replace("\"", "'").replace("/", "__")
    fname = info_dict["id"] + "-" + replaced_title + ".mp4"
    if os.path.exists(old_fname):
        assert(os.path.exists(old_fname))
        os.rename(old_fname, fname)
    fsize = os.path.getsize(fname)

    target_size = FSIZE_TARGET
    if fsize > target_size:
        new_file_name = trimming_video_to_8MB(fname)
        return ((fname, new_file_name), True, info_dict)
    return ((fname, None), False, info_dict)



if __name__ == '__main__':
    head_fname = "__out__big__2__"
    print("hello world")
    # url = "https://www.youtube.com/watch?v=XCs7FacjHQY"
    urls = [
        "https://vt.tiktok.com/ZSJgGCR9S/",
        "https://vt.tiktok.com/ZSJgGvR7c/"
    ]
    ydlmp4 = youtube_dl.YoutubeDL(
        {
            # 'outtmpl': head_fname + '.mp4',
            'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'verbose': True,
            'format': "0",
            'outtmpl': "%(id)s.%(ext)s"
        })

    num = 1
    for url in urls:
        info_dict = ydlmp4.extract_info(url, download=True)
        with open("out_tiktok_" + str(num) + ".json", 'w') as f:
            json.dump(info_dict, f, ensure_ascii=False)
        num += 1
