import requests

if __name__ == "__main__":
    target_url = "https://lap78.ask.fm/igoto/45DKECPW7B667HQMHN2IG6NM6SDD7LCJ2P667BP7D7SLNZN62UYY2Z2IF5H4YRZSKC67YFQIJQUH4DB7YEV7M2VONS5LPBQLUIORJE2YHVWSCKGPBOHXYPXKSC27R6LPZSRYGEIXRKEH3H4IBOBB6QK46PGHLYM4ZDPVJMTRQSO2OPPSIUYFB5HK5NNIJ4H3TI43KFDU4EKQ===="
    data = requests.get(target_url)
    text = data.text
    print(f"type of text: {type(text)}")
    with open("dump_ask1.txt", "w") as f:
        f.write(text)
