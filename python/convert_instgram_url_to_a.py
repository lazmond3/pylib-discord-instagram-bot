# __a にアクセスする関数
import re

def make_a_url(url):
    # https://www.instagram.com/p/CJ8u5PCH-WG/?utm_source=ig_web_copy_link
    m = re.match(r"https://www.instagram.com/p/([^/])+", url)
    if m:
        new_url = m.group(0) + "/?__a=1"
        return new_url
    return None
if __name__ == "__main__":
        print("make: ", make_a_url("https://www.instagram.com/p/CJ8u5PCH-WG/?utm_source=ig_web_copy_link"))