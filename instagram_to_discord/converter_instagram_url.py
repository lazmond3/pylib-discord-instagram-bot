# __a にアクセスする関数
import re
from debug import DEBUG


def convert_instagram_url_to_a(url):
    # https://www.instagram.com/p/CJ8u5PCH-WG/?utm_source=ig_web_copy_link
    m = re.match(r"https://www.instagram.com/(p|reel)/([^/])+", url)
    if m:
        new_url = m.group(0) + "/?__a=1"
        return new_url
    return None


def instagram_make_base_url(url):
    m = re.match(r"https://www.instagram.com/(p|reel)/([^/])+", url)
    if m:
        new_url = m.group(0)
        return new_url
    return None


def extract_url(line: str):
    m = re.match(r"^.*(https://www.instagram.com/(p|reel)/([^/])+).*$", line)
    if m:
        return m.group(1)
    else:
        return None


def instagram_extract_from_content(content: str):
    for line in content.split("\n"):
        if DEBUG:
            print("[debug extract from..] line: {}".format(line))
        base_url = extract_url(line)
        if base_url:
            return base_url
    return None


def instagram_make_author_page(username):
    return f"https://www.instagram.com/{username}/"


if __name__ == "__main__":
    print("make: ", convert_instagram_url_to_a(
        "https://www.instagram.com/p/CJ8u5PCH-WG/?utm_source=ig_web_copy_link"))
    print("make: ", convert_instagram_url_to_a(
        "https://www.instagram.com/reel/CJ8u5PCH-WG/?utm_source=ig_web_copy_link"))
    print("extract: ", extract_url(
        "https://www.instagram.com/reel/CJ8u5PCH-WG/?utm_source=ig_web_copy_link"))
