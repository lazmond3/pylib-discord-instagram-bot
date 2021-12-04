import json
from typing import List

from dict2obj import Dict2Obj
from dataclasses import dataclass


@dataclass
class InstagramData:
    """[summary]

    Attributes
    -----------
    media: :class:`str`
        The url for the post's media.
    is_video: :class:`boolean`
        Whether this includes a video post.
    caption: :class:`str`
        The description by the author.
    """
    media: str
    is_video: bool
    is_video_for_first: bool
    caption: str
    profile_url: str
    username: str
    full_name: str
    video_url: str
    media_urls: List[str]

    def __str__(self):
        n_caption = " ".join(self.caption[:100].split("\n"))
        return f"""
==================================================
    media: {self.media}
==================================================
    is_video: {self.is_video}
==================================================
    caption: {n_caption}
==================================================
    profile_url: {self.profile_url}
==================================================
    username: {self.username}
==================================================
    full_name: {self.full_name}
==================================================
    video_url: {self.video_url}
==================================================
    media_urls: {", ".join(self.media_urls)}
==================================================
        """

    def __init__(
        self, media, is_video, caption, profile_url, username, full_name, video_url
    ):
        """init
        media: 写真投稿に対する メイン画像 url
        is_video: ビデオかどうか
        caption: キャプション(投稿時のメッセージ)
        self.profile_url = profile_url # プロフィール画像のurl
        self.username = username # ユーザネーム(アルファベット)
        self.full_name = full_name # 表示名
        """
        self.media = media  # 写真投稿に対する メイン画像 url
        self.is_video = is_video  # ビデオかどうか
        self.caption = caption  # キャプション(投稿時のメッセージ)
        self.profile_url = profile_url  # プロフィール画像のurl
        self.username = username  # ユーザネーム(アルファベット)
        self.full_name = full_name  # 表示名
        self.video_url = video_url
        self.media_urls = []
        self.is_video_for_first = is_video


def convert_long_caption(caption: str) -> str:
    lst = caption.split("\n")
    lines = len(lst)
    if lines > 10:
        return "\n".join(lst[:10])
    else:
        return caption


def convert_to_instagram_type(oj) -> InstagramData:
    media = oj.graphql.shortcode_media.display_url
    if len(oj.graphql.shortcode_media.edge_media_to_caption.edges) == 0:
        caption = ""
    else:
        caption = oj.graphql.shortcode_media.edge_media_to_caption.edges[0].node.text

    caption = convert_long_caption(caption)
    is_video = oj.graphql.shortcode_media.is_video
    # TODO: 途中だけvideo の場合
    # shortcode_media.edge_sidecar_to_children.edges
    # [0].node.video_url が入る.

    profile_url = oj.graphql.shortcode_media.owner.profile_pic_url
    username = oj.graphql.shortcode_media.owner.username
    full_name = oj.graphql.shortcode_media.owner.full_name
    if is_video:
        video_url = oj.graphql.shortcode_media.video_url
    else:
        video_url = None
    return InstagramData(
        media=media,
        is_video=is_video,
        caption=caption,
        profile_url=profile_url,
        username=username,
        full_name=full_name,
        video_url=video_url,
    )


def get_multiple_medias(oj) -> List[str]:
    ans = []
    if hasattr(oj.graphql.shortcode_media, "edge_sidecar_to_children"):
        for node in oj.graphql.shortcode_media.edge_sidecar_to_children.edges:
            display_url = node.node.display_url
            ans.append(display_url)
        return ans
    else:
        media = oj.graphql.shortcode_media.display_url
        return [media]


def get_multiple_medias_from_str(str_arg) -> List[str]:
    dic_ = json.loads(str_arg)
    oj = Dict2Obj(dic_)
    return get_multiple_medias(oj)


def convert_json_str_to_obj(str_):
    dic_ = json.loads(str_)
    return Dict2Obj(dic_)


def instagram_parse_json_to_obj(str):
    """
    __a=1 の json レスポンスを InstagramData に変換する。
    """
    dic_ = json.loads(str)
    oj = Dict2Obj(dic_)
    return convert_to_instagram_type(oj)


if __name__ == "__main__":
    import json

    with open("yoshioka.json") as f:
        dic_ = json.load(f)
    with open("instagram_multi_img.json") as f:
        str_ = f.read()
    oj = Dict2Obj(dic_)

    for i in get_multiple_medias(oj):
        print(i)
    # for i in get_multiple_medias_from_str(str_):
    #     print(i)
    # print(get_multiple_medias(oj))
