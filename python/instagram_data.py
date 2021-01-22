class InstagramData:
    def __str__(self):
        n_caption = " ".join(self.caption[:100].split("\n"))
        return(f"""
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
        """)
    def __init__(self, 
    media,
    is_video,
    caption,
    profile_url,
    username,
    full_name
    ):
        self.media = media
        self.is_video = is_video
        self.caption = caption
        self.profile_url = profile_url
        self.username = username
        self.full_name = full_name

def convert_to_instagram_data(oj):
    media = oj.graphql.shortcode_media.display_url
    caption = oj.graphql.shortcode_media.edge_media_to_caption.edges[0].node.text
    is_video = oj.graphql.shortcode_media.is_video
    profile_url = oj.graphql.shortcode_media.owner.profile_pic_url
    username = oj.graphql.shortcode_media.owner.username
    full_name = oj.graphql.shortcode_media.owner.full_name
    return InstagramData(
        media = media,
        is_video = is_video,
        caption = caption,
        profile_url = profile_url,
        username = username,
        full_name = full_name
    )
if __name__ == "__main__":
    from sample_insta_obj import sample_isnta_obj
    print(convert_to_instagram_data(sample_isnta_obj))