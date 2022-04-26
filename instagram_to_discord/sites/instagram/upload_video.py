import os
from instagram_to_discord.boto3 import upload_video_file
from instagram_to_discord.download import (
    download_file,
    make_instagram_mp4_filename,
    save_image,
)


def upload_instagram_video(video_url: str) -> str:
    pass
    fname_video = make_instagram_mp4_filename("dump_videos_instagram", video_url)
    video_content = download_file(video_url)
    save_image(fname_video, video_content)
    fsize = os.path.getsize(fname_video)

    video_s3_url = upload_video_file(fname_video)
    return video_s3_url
