import os

import requests


# あとで移動する
# https://qiita.com/donksite/items/21852b2baa94c94ffcbe
def download_file(url, timeout=10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e
    return response.content


# 動画のファイル名を決める
def make_twitter_mp4_filename(base_dir, num, url):
    ext = os.path.splitext(url)[1]  # 拡張子を取得
    filename = str(num) + ext  # 番号に拡張子をつけてファイル名にする

    fullpath = os.path.join(base_dir, filename)
    return fullpath

# 画像のファイル名を決める
def make_twitter_image_filename(base_dir:str, tweet_num:str, index:int, url:str):
    ext = os.path.splitext(url)[1]  # 拡張子を取得
    filename = f"{tweet_num}_{index}{ext}"  # 番号に拡張子をつけてファイル名にする

    fullpath = os.path.join(base_dir, filename)
    return fullpath


# 画像のファイル名を決める
def make_instagram_mp4_filename(base_dir, url):
    if "?" in url:
        url = url.split("?")[0]
    ext = os.path.splitext(url)[1]  # 拡張子を取得. ドット含めている
    basename = os.path.basename(url).split(".")[0]
    filename = basename + ext  # 番号に拡張子をつけてファイル名にする

    fullpath = os.path.join(base_dir, filename)
    return fullpath


# 画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

if __name__ == "__main__":
    url = "https://pbs.twimg.com/media/FEEnu0zaQAMfXHy.jpg"
    image_data = download_file(url)
    tweet_num = "1459491452048740352"
    idx = 1
    fname = make_twitter_image_filename("", tweet_num, idx, url )
    print(f"fname: {fname}")
    # save_image("sample.jpg", image_data )
    save_image(fname, image_data )
    from .boto3 import upload_image_file
    upload_image_file(fname, tweet_num, idx)
