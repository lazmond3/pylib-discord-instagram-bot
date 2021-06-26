import requests
import os

# あとで移動する
# https://qiita.com/donksite/items/21852b2baa94c94ffcbe
def download_image(url, timeout = 10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e
    return response.content

# 画像のファイル名を決める
def make_filename(base_dir, num, url):
    ext = os.path.splitext(url)[1] # 拡張子を取得
    filename =  str(num) + ext        # 番号に拡張子をつけてファイル名にする

    fullpath = os.path.join(base_dir, filename)
    return fullpath

# 画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)
