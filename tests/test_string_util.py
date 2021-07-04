# -*- coding: utf-8 -*-

# from .context import use_hello
import unittest
from . import context
from debug import DEBUG
instagram_to_discord = context.instagram_to_discord


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_sophisticate(self):
        cap_to = instagram_to_discord.string_util.sophisticate_string(
            get_caption()
        )
        answer = """【美女navi ☻*】
今回ご紹介させていただく方は❤︎
まぁみ(小田愛実) さん ▶︎▷ @maaaami79
# Repost
#gyda
まぁみ(小田愛実) さんのアカウントには
他にも素敵な投稿が(*´﹀`)
ぜひ覗いてみてくださいね🧡
掲載希望の方は⇒
@bijo_navi ❤︎と
# ビジョナビ タグ付けお願いします☺︎!!
次回もお楽しみに...😍
#美肌 #カラコン #金髪 #ロングヘア
#スタイル抜群 #巻き髪
#ギャルメイク #笑顔 #振り向き美人
#アイメイク #マツエク #美意識
#赤リップ #コスメ #naturalbeauty
#セルフィー #美容 #リップ #howto
#ヘアスタイル #おしゃれ女子
#大人メイク #メイク #オトナ女子
#美意識向上 #大人可愛い
#セルフィー女子 #女子力アップ"""
        if DEBUG:
            print(f"answer ({len(answer)}):", answer)
            print(f"capto ({len(cap_to)}):", cap_to)
            # with open("write", "w") as f:
            #     f.write(cap_to)
        assert answer == cap_to


def get_caption():
    return "*\n*\n【美女navi ☻*】\n*\n*\n今回ご紹介させていただく方は❤︎\nまぁみ(小田愛実) さん ▶︎▷ @maaaami79\n * \n * \n# Repost\n.\n.\n#gyda \n.\n.\n.\n.\nまぁみ(小田愛実) さんのアカウントには\n他にも素敵な投稿が(*´﹀`)\nぜひ覗いてみてくださいね🧡\n*\n*\n*\n掲載希望の方は⇒\n@bijo_navi ❤︎と\n# ビジョナビ タグ付けお願いします☺︎!!\n*\n*\n次回もお楽しみに...😍\n*\n*\n#美肌 #カラコン #金髪 #ロングヘア\n#スタイル抜群 #巻き髪　\n#ギャルメイク #笑顔 #振り向き美人\n#アイメイク #マツエク #美意識\n#赤リップ #コスメ #naturalbeauty\n#セルフィー #美容 #リップ #howto\n#ヘアスタイル #おしゃれ女子\n#大人メイク #メイク #オトナ女子\n#美意識向上 #大人可愛い\n#セルフィー女子 #女子力アップ"


if __name__ == '__main__':
    unittest.main()
