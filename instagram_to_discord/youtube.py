import youtube_dl
import moviepy.editor as mp
import os
import json
import re
# import ffmpeg
import subprocess
from typing import Tuple, Dict
from . import FSIZE_TARGET

# 欲しい関数について
# - download_youtube_video => fname / fpath
# TODO: youtube の 画面情報, description, author を指定, プロフィール画像、サムネ
# サムネはないけど、
# description, uplaod_date, duration, view_count, averate_rating, like_count, dislike_count

def extract_youtube_url(text:str) -> str:
    m = re.match(r".*(https://www.youtube.com/watch\?v=[^&]+)&?.*", text)
    if m:
        url = m.group(1)
        return url
    raise Exception("[extract_youtube_url] failed for text: " + text)


# 2つ目の値は、 fsize が 8MBを超えているか ( (fname, full fname), over 8MB, info_dict)
def download_youtube_video(url: str) -> Tuple[Tuple[str], bool, Dict[str, any]]:
    ydlmp4 = youtube_dl.YoutubeDL(
        {
            # 'outtmpl': head_fname + '.mp4',
            'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'verbose': True,
            'format': "18"
        })
    info_dict = ydlmp4.extract_info(url, download=True)
    withspace_fname = info_dict["title"] + "-" + info_dict["id"] + ".mp4"
    fname = info_dict["title"].replace(" ", "_").replace("　", "__") + "-" + info_dict["id"] + ".mp4"
    os.rename(withspace_fname, fname)
    fsize = os.path.getsize(fname)
    current_duration: int = info_dict["duration"]

    target_size = FSIZE_TARGET
    if fsize > target_size:
        target_duration_f: float = float(target_size) / fsize * current_duration
        target_duration:int = int(target_duration_f)
        new_file_name = fname.split(".")[0] + "-trimmed" + ".mp4"
        subprocess.run(["ffmpeg", "-i", fname, "-t", str(target_duration), "-c", "copy", new_file_name])
        return ((fname, new_file_name), True, info_dict)
    return ((fname, None), False, info_dict)




if __name__ == '__main__':
    head_fname = "__out__big__2__"
    print("hello world")
    # url = "https://www.youtube.com/watch?v=XCs7FacjHQY"
    import sys
    urls = [
    "https://www.youtube.com/watch?v=XCs7FacjHQY",
    "https://www.youtube.com/watch?v=mHuiJGGAJoE",
    "https://www.youtube.com/watch?v=2Ly4yDzN4xM",
    ]
    ydlmp4 = youtube_dl.YoutubeDL(
        {
            # 'outtmpl': head_fname + '.mp4',
            'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'verbose': True,
            'format': "18"
        })
    num = 0
    for url in urls:
        info_dict = ydlmp4.extract_info(url, download=True)
        with open("out" + str(num) + ".json", 'w') as f:
            json.dump(info_dict, f, ensure_ascii=False)
        num += 1
        # just for debug
        # for fmt in info_dict["formats"]:
        #     if fmt["acodec"] != "none" and not "audio only" in fmt["format"]:
        #         print(fmt["format"], fmt["acodec"])
        # print("file size: ", str(fsize / (10**6)) + "MB")
        fname = info_dict["title"] + "-" + info_dict["id"] + ".mp4"
        fsize = os.path.getsize(fname)
        current_duration: int = info_dict["duration"]

        target_size = 7.999 * (10 ** 6)
        if fsize > target_size:
            target_duration_f: float = float(target_size) / fsize * current_duration
            target_duration:int = int(target_duration_f)
            new_file_name = fname.split(".")[0] + "-trimmed" + ".mp4"
            result = subprocess.run(["ffmpeg", "-i", fname, "-t", str(target_duration), "-c", "copy", new_file_name])
            print("result: ", result)

    # ydl_opts = {
    #     'format': 'bestaudio/best',
    #     'outtmpl':  head_fname + '.%(ext)s',
    #     'postprocessors': [
    #         {'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192'},
    #         {'key': 'FFmpegMetadata'},
    #     ],
    # }

    # ydlmp3 = youtube_dl.YoutubeDL(ydl_opts)
    # info_dict = ydlmp3.extract_info(url, download=False)
    # print(info_dict)
    # with open("out.json", 'r') as f:
        # info_dict = json.load(f)
    
    
    #mp4として出力されてものに.mp4を付ける
    # os.rename('out', head_fname + ".mp4")

    #映像と音声を合わせる
    # clip = mp.VideoFileClip( head_fname + '.mp4').subclip()
    # clip.write_videofile(head_fname + "_new_" + '.mp4', audio= head_fname + '.mp3')



"""
$ youtube-dl -F https://www.youtube.com/watch?v=XCs7FacjHQY
[youtube] XCs7FacjHQY: Downloading webpage
[info] Available formats for XCs7FacjHQY:
format code  extension  resolution note
249          webm       audio only tiny   49k , webm_dash container, opus @ 49k (48000Hz), 1.73MiB
250          webm       audio only tiny   65k , webm_dash container, opus @ 65k (48000Hz), 2.29MiB
140          m4a        audio only tiny  129k , m4a_dash container, mp4a.40.2@129k (44100Hz), 4.53MiB
251          webm       audio only tiny  129k , webm_dash container, opus @129k (48000Hz), 4.54MiB
394          mp4        256x144    144p   70k , mp4_dash container, av01.0.00M.08@  70k, 24fps, video only, 2.45MiB
278          webm       256x144    144p   85k , webm_dash container, vp9@  85k, 24fps, video only, 2.99MiB
160          mp4        256x144    144p  103k , mp4_dash container, avc1.4d400c@ 103k, 24fps, video only, 3.62MiB
395          mp4        426x240    240p  152k , mp4_dash container, av01.0.00M.08@ 152k, 24fps, video only, 5.32MiB
242          webm       426x240    240p  185k , webm_dash container, vp9@ 185k, 24fps, video only, 6.49MiB
133          mp4        426x240    240p  227k , mp4_dash container, avc1.4d4015@ 227k, 24fps, video only, 7.97MiB
396          mp4        640x360    360p  327k , mp4_dash container, av01.0.01M.08@ 327k, 24fps, video only, 11.45MiB
243          webm       640x360    360p  404k , webm_dash container, vp9@ 404k, 24fps, video only, 14.15MiB
134          mp4        640x360    360p  545k , mp4_dash container, avc1.4d401e@ 545k, 24fps, video only, 19.07MiB
397          mp4        854x480    480p  605k , mp4_dash container, av01.0.04M.08@ 605k, 24fps, video only, 21.16MiB
244          webm       854x480    480p  734k , webm_dash container, vp9@ 734k, 24fps, video only, 25.66MiB
135          mp4        854x480    480p  929k , mp4_dash container, avc1.4d401e@ 929k, 24fps, video only, 32.48MiB
398          mp4        1280x720   720p 1128k , mp4_dash container, av01.0.05M.08@1128k, 24fps, video only, 39.44MiB
247          webm       1280x720   720p 1472k , webm_dash container, vp9@1472k, 24fps, video only, 51.45MiB
136          mp4        1280x720   720p 1560k , mp4_dash container, avc1.4d401f@1560k, 24fps, video only, 54.54MiB
399          mp4        1920x1080  1080p 2002k , mp4_dash container, av01.0.08M.08@2002k, 24fps, video only, 69.99MiB
248          webm       1920x1080  1080p 2565k , webm_dash container, vp9@2565k, 24fps, video only, 89.68MiB
137          mp4        1920x1080  1080p 3902k , mp4_dash container, avc1.640028@3902k, 24fps, video only, 136.41MiB
400          mp4        2560x1440  1440p 6659k , mp4_dash container, av01.0.12M.08@6659k, 24fps, video only, 232.78MiB
271          webm       2560x1440  1440p 8097k , webm_dash container, vp9@8097k, 24fps, video only, 283.04MiB
401          mp4        3840x2160  2160p 12959k , mp4_dash container, av01.0.12M.08@12959k, 24fps, video only, 452.97MiB
313          webm       3840x2160  2160p 16974k , webm_dash container, vp9@16974k, 24fps, video only, 593.30MiB
18           mp4        640x360    360p  734k , avc1.42001E, 24fps, mp4a.40.2 (44100Hz), 25.69MiB (best)
"""