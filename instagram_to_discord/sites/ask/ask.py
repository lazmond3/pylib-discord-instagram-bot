import requests
from bs4 import BeautifulSoup

def get_ask_html_text_from_url(url: str):
    """url -> str text"""
    data = requests.get(url)
    return data.text


def process_question_and_answer_from_text(text: str):
    """text -> q,ans"""
    soup = BeautifulSoup(text, "html.parser")
    q = soup.select_one("title")
    q_text = q.text
    q_text = q_text[:q_text.find(" | ask.fm")]
    
    # こちらだと尻切れだった
    # ans =soup.select_one("meta[name='description']")["content"]

    ans =soup.select_one("div.streamItem_content").text
    return q_text, ans


if __name__ == "__main__":
    target_url = "https://lap78.ask.fm/igoto/45DKECPW7B667HQMHN2IG6NM6SDD7LCJ2P667BP7D7SLNZN62UYY2Z2IF5H4YRZSKC67YFQIJQUH4DB7YEV7M2VONS5LPBQLUIORJE2YHVWSCKGPBOHXYPXKSC27R6LPZSRYGEIXRKEH3H4IBOBB6QK46PGHLYM4ZDPVJMTRQSO2OPPSIUYFB5HK5NNIJ4H3TI43KFDU4EKQ===="
    target_url = "https://lap78.ask.fm/igoto/45DKECPW7B667HQMHN2IG6NM6SDD7LCJ2P667BP7D7SLNZN62UYY2Z2JFBBMWRB3K6YP6FIGJQUH4DB7YEV7M2VONS5LPBQLUIORJE2YHVWSCKGPBOHXYPXKSC27R6LPZSRYGEIXRKEH3H4IBOBB6QK46PGHLYM4ZDPVJMTRQSO2OPPSIUYFB5HK5NNIJ4H3TI43KFDU4EKQ===="
    data = requests.get(target_url)
    text = data.text
    print(f"type of text: {type(text)}")
    with open("dump_ask/dump_ask2.txt", "w") as f:
        f.write(text)
    # exit(0)
    text = ""
    with open("dump_ask/dump_ask2.txt") as f:
        text = f.read()
    
    soup = BeautifulSoup(text, "html.parser")

    q = soup.select_one("title")
    q_text = q.text
    q_text = q_text[:q_text.find(" | ask.fm")]
    print(f"title: {q_text}")
    r = soup.select_one("div.streamItem_content")
    print(f"r: ", r.text)
    print(f"r: ", soup.select_one("meta[name='description']")["content"])
    