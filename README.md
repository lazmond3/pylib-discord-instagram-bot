# Usage

```bash

# install
python3 setup.py install
# or
pip3 -r requirements.txt


# execution
REDIS_PASS=$REDIS_PASS \
  TOKEN=$DISCORD_BOT_TOKEN \
  DEBUG=1 \
  COOKIE_PATH=cookie2.txt \
  python3 -m instagram_to_discord
```

## クッキーファイルの中身

```txt
mid=XX...; sessionid=6788562761...
```

# 2021/01/24 日 02:25]

## DOING

- cookie を get env 経由で..

- discord.py はだいぶ使えるようになった。
- [x] instagram parse が下手で、
  - [x] title
  - [x] url の取得 ( これは obj には入れないよね？ )
  - [x] author url (そんなに重要ではないのでなくてもいい)
        というのを加えよう。

あと、kzm_random じゃなくて、 vc のみにする。

## パッケージ化 について

- getenv でなんとかしていく assert で落とす
  - token を利用する。

# 2021/01/23 土 23:50]

## DOING

- instagram_type を ライブラリ化

# 2021/01/22 金 10:30]

## DOING

- dict2obj の解決
