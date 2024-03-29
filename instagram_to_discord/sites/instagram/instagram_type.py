import json
from dataclasses import dataclass
from typing import List
from ...logging import log as logger

from dict2obj import Dict2Obj


@dataclass
class InstagramInnerNode:
    url: str
    is_video: bool
    display_url: str = ""


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
    medias: List[InstagramInnerNode]

    def __str__(self):
        n_caption = " ".join(self.caption[:100].split("\n"))
        newline_tab = "\n\t"
        media_lines = ""
        for i, m in enumerate(self.medias):
            media_lines += f"[{i+1:02d}] {m.url}"
            if i != len(self.medias) - 1:
                media_lines += newline_tab
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
    media_urls: {newline_tab}{media_lines}
==================================================
    """

    def __init__(
        self,
        media,
        is_video,
        caption,
        profile_url,
        username,
        full_name,
        video_url,
        medias,
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
        self.is_video_for_first = is_video  # rename した要素を追加した。
        self.caption = caption  # キャプション(投稿時のメッセージ)
        self.profile_url = profile_url  # プロフィール画像のurl
        self.username = username  # ユーザネーム(アルファベット)
        self.full_name = full_name  # 表示名
        self.video_url = video_url
        self.medias = medias


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
    profile_url = oj.graphql.shortcode_media.owner.profile_pic_url
    username = oj.graphql.shortcode_media.owner.username
    full_name = oj.graphql.shortcode_media.owner.full_name

    # 新規追加
    medias: List[InstagramInnerNode] = get_multiple_mediasV2(oj)

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
        medias=medias,
    )


def convert_to_instagram_type_v2(oj) -> InstagramData:
    """
    1/25 以降の `graphQL` がなくなったバージョン
    """

    items = oj.items
    item = items[0]

    # media = oj.graphql.shortcode_media.display_url
    #     caption = ""
    # if len(oj.graphql.shortcode_media.edge_media_to_caption.edges) == 0:
    # else:
    #     caption = oj.graphql.shortcode_media.edge_media_to_caption.edges[0].node.text

    if item.caption:
        caption = item.caption.text
    else:
        caption = ""
    caption = convert_long_caption(caption)

    is_video = item.media_type == 2
    is_carousel_media = hasattr(item, ("carousel_media"))
    # is_multi_carousel
    if is_carousel_media:  # メインの画像
        images = sorted(
            item.carousel_media[0].image_versions2.candidates, key=lambda x: -x.height
        )
        media = images[0].url
    else:
        images = sorted(item.image_versions2.candidates, key=lambda x: -x.height)
        media = images[0].url

    profile_url = item.user.profile_pic_url
    username = item.user.username
    full_name = item.user.full_name

    # 新規追加
    medias: List[InstagramInnerNode] = get_multiple_medias_v3(is_carousel_media, item)

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
        medias=medias,
    )


def get_multiple_medias(oj) -> List[str]:
    medias = get_multiple_mediasV2(oj)
    ans_list = []
    for m in medias:
        ans_list.append(m.url)
    return ans_list
    # ans = []
    # if hasattr(oj.graphql.shortcode_media, "edge_sidecar_to_children"):
    #     for node in oj.graphql.shortcode_media.edge_sidecar_to_children.edges:
    #         display_url = node.node.display_url
    #         ans.append(display_url)
    #     return ans
    # else:
    #     media = oj.graphql.shortcode_media.display_url
    #     return [media]


def get_multiple_mediasV2(oj) -> List[InstagramInnerNode]:
    """oj から それぞれのnodeが動画かどうか判定する"""
    ans = []
    if hasattr(oj.graphql.shortcode_media, "edge_sidecar_to_children"):
        for node in oj.graphql.shortcode_media.edge_sidecar_to_children.edges:
            if node.node.is_video:
                inst_node = InstagramInnerNode(
                    url=node.node.video_url,
                    is_video=True,
                    display_url=node.node.display_url,
                )
            else:
                display_resources = node.node.display_resources
                max_resolution = sorted(
                    display_resources, key=lambda x: -x.config_height
                )[0]
                inst_node = InstagramInnerNode(
                    # url=node.node.display_url,
                    # display_url=node.node.display_url
                    url=max_resolution.src,
                    display_url=max_resolution.src,
                    is_video=False,
                )
            ans.append(inst_node)
        return ans
    else:
        display_resources = oj.graphql.shortcode_media.display_resources
        max_resolution = sorted(display_resources, key=lambda x: -x.config_height)[0]

        return [
            InstagramInnerNode(
                is_video=False,
                url=max_resolution.src,
                display_url=max_resolution.src
                # url=media,
                # display_url=media
            )
        ]


def get_multiple_medias_v3(is_carousel_media: bool, item) -> List[InstagramInnerNode]:
    """oj から それぞれのnodeが動画かどうか判定する"""
    ans = []
    if is_carousel_media:
        logger.info(f"item: {item} id: {item.id}")
        logger.info(f"carousel_media_count: {item.carousel_media_count}")
        for node in item.carousel_media:
            if node.media_type == 1:  # 画像のとき
                images = sorted(node.image_versions2.candidates, key=lambda x: -x.width)
                max_image = images[0]

                inst_node = InstagramInnerNode(
                    url=max_image.url, is_video=False, display_url=max_image.url
                )
            else:  # 動画の時
                images = sorted(node.image_versions2.candidates, key=lambda x: -x.width)
                max_image = images[0]

                max_resolution_video = sorted(
                    node.video_versions, key=lambda x: -x.height
                )[0]
                inst_node = InstagramInnerNode(
                    url=max_resolution_video.url,
                    display_url=max_image.url,
                    is_video=True,
                )
            ans.append(inst_node)
        return ans
    else:
        if item.media_type == 1:  # 画像
            images = sorted(item.image_versions2.candidates, key=lambda x: -x.width)
            max_image = images[0]
            inst_node = InstagramInnerNode(
                url=max_image.url,
                display_url=max_image.url,
                is_video=False,
            )
            return [inst_node]
        else:
            images = sorted(item.image_versions2.candidates, key=lambda x: -x.width)
            max_image = images[0]

            max_resolution_video = sorted(item.video_versions, key=lambda x: -x.height)[
                0
            ]
            inst_node = InstagramInnerNode(
                url=max_resolution_video.url,
                display_url=max_image.url,
                is_video=True,
            )
            return [inst_node]


def get_multiple_medias_from_str(str_arg) -> List[str]:
    dic_ = json.loads(str_arg)
    oj = Dict2Obj(dic_)
    return get_multiple_medias(oj)


def get_multiple_mediasV2_from_str(str_arg) -> List[InstagramInnerNode]:
    dic_ = json.loads(str_arg)
    oj = Dict2Obj(dic_)
    return get_multiple_mediasV2(oj)


def get_multiple_medias_v3_from_str(str_arg) -> List[InstagramInnerNode]:
    dic_ = json.loads(str_arg)
    oj = Dict2Obj(dic_)
    is_carousel_media = hasattr(oj.items[0], ("carousel_media"))
    return get_multiple_medias_v3(is_carousel_media, oj.items[0])


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


def instagram_parse_json_to_obj_v2(str):
    """
    1/25 以降の graphQLがなくなったバージョン
    __a=1 の json レスポンスを InstagramData に変換する。
    """
    dic_ = json.loads(str)
    oj = Dict2Obj(dic_)
    return convert_to_instagram_type_v2(oj)


if __name__ == "__main__":
    with open("tests/data/instagram_multiple_image_and_video_佐々木希.json") as f:
        dic_ = json.load(f)
    # with open("instagram_multi_img.json") as f:
    #     str_ = f.read()
    oj = Dict2Obj(dic_)
    inObj = convert_to_instagram_type(oj)
    print(f"inObj: {inObj}")
    # import json

    # with open("yoshioka.json") as f:
    #     dic_ = json.load(f)
    # with open("instagram_multi_img.json") as f:
    #     str_ = f.read()
    # oj = Dict2Obj(dic_)

    # for i in get_multiple_medias(oj):
    #     print(i)
    # # for i in get_multiple_medias_from_str(str_):
    # #     print(i)
    # # print(get_multiple_medias(oj))
