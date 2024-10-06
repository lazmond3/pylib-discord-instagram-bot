# What this is

This is a Discord bot that retrieves images from Twitter and Instagram URLs and reposts them.

| what | architecture |
| --- | --- |
|  <img src="https://github.com/user-attachments/assets/cd33ee0f-1351-4f8d-9b95-61fc7c0dfa8e" width=500> |  <img src="https://github.com/user-attachments/assets/5268c2ec-9631-4af1-a262-b907a0b66587" width=500> |


# 使い方 (how to use)

```bash
# DEPENDS ON...
# - dict2obj (easier to access json object)
# - discord.py (bot)
# - requests (access to instagram)
# - boto3 (upload images and videos to s3)
# - youtube_dl (download youtube, tiktok)
# - ffmpeg (truncate video to sizing limitation for attachment)
# - black (format)
# - flake8 (linter)
# - autopep8 (linter)
# - isort (format)
# - beautifulsoup4 (parse html; for ask.fm)
# - pytest... (unit test)
# - elasticsearch, CMRESHandler (logging to elasticsearch)
pip3 -r requirements.txt

# WHEN RUN ON LOCAL(log output to stdout, else to elasticsearch)
IS_DEBUG=1 ENV=local TOKEN=$TOKEN python3 -m instagram_to_discord
```

## 動作する機能 FUNCTIONS
- twitter の URL を post したあとに、自動でS3にアーカイブした動画URLを投稿する。(NSFWでない限り、自動でプレビューされる)
- twitter の URL を post したあとに、数字を post すると、当該インデックスの画像を投稿する（スマホで閲覧すると、プレビュー画像は1枚目しか表示されないため、他の画像への言及であることを強調したいときに使う)

>- After posting a twitter URL, post the video URL archived to S3. (Unless it's NSFW, it will be previewed automatically by discord app)
>- If you post a number/numbers(index, comma seperated) after posting a twitter URL, the image(s) those index(indices) indicates will be posted. (When you view discord on a smartphone, only the first preview image is displayed, so use this when you want to emphasize that it is a reference to other images.)


## DEPRECATED: important JSON paths
この項目は、instagram API の `__a=1` が廃止されたため、古くなりました。

> This item is obsolete due to the deprecation of __a=1 in the instagram API.

- `edge_sidecar_to_children.edges[].node.display_url`
- `edge_sidecar_to_children.edges[].node.display_url`

