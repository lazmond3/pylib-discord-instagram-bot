# ダンプ
https://www.instagram.com/p/CQdnVrkHZOC/?utm_source=ig_web_copy_link&__a=1 こちらのファイルを, instagram_multi_img.json こちらに

複数画像は、
```
edge_sidecar_to_children.edges[].node.display_url 
```
あたりにあるっぽい.

# TODO
- [ ] env を一括でexport するようにする
- [ ] 後続で画像idxを指定するとき、s3を利用できていない。
- [ ] terraform のモジュールを検討する。
- [ ] ほか、適宜リファクタする。

# Usage

```bash

pip3 -r requirements.txt


# execution
REDIS_PASS=$REDIS_PASS \
  TOKEN=$DISCORD_BOT_TOKEN \
  DEBUG=1 \
  COOKIE_PATH=cookie2.txt \
  python3 -m instagram_to_discord
```
