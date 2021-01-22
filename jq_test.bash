# 画像
cat sample__a.json  | jq .graphql.shortcode_media.display_url
# display_resources で config_width のint数値が最大の ものの src を選ぶ。

# is_video
# edge_media_to_caption.edges[0].node.text

# owner
# .profile_pic_url
# .username
# .full_name