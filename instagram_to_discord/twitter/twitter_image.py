from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TwitterImage:
    id_str: str
    image_urls: List[str]
    video_url: str
    user_display_name: str
    user_screen_name: str
    user_url: str
    user_profile_image_url: str
    text: str


# 入力は js_dict
def convert_twitter(dic: Dict[str, Any]) -> TwitterImage:
    images: Dict[str, str] = dic["extended_entities"]["media"]
    user_display_name = dic["user"]["name"]
    user_screen_name = dic["user"]["screen_name"]
    user_url = f"https://twitter.com/{user_screen_name}"
    user_profile_image_url = dic["user"]["profile_image_url_https"]
    text = dic["full_text"]

    video_url_inner: str = ""
    image_url_inner: str = ""
    image_urls: List[str] = []
    if "video_info" in dic["extended_entities"]["media"][0]:
        video_info: Dict[str, List[Dict[str, str]]] = dic["extended_entities"]["media"][
            0
        ]["video_info"]
        variants: List[Dict[str, str]] = video_info["variants"]
        video_mp4_list: List[Dict[str, str]] = list(
            filter(lambda x: x["content_type"] == "video/mp4", variants)
        )
        # ビットレート最大を取得
        video_mp4_list = sorted(video_mp4_list, key=lambda x: -int(x["bitrate"]))

        video_url_inner = video_mp4_list[0]["url"]
        image_url_inner = dic["extended_entities"]["media"][0]["media_url_https"]
        image_urls = [image_url_inner]
    else:
        image_urls = list(map(lambda x: images["media_url_https"], images.keys()))
        # print("[debug][image_urls]: ", image_urls)

    return TwitterImage(
        id_str=dic["id_str"],
        image_urls=image_urls,
        video_url=video_url_inner,
        user_display_name=user_display_name,
        user_screen_name=user_screen_name,
        user_url=user_url,
        user_profile_image_url=user_profile_image_url,
        text=text,
    )
