from instagram_to_discord.sites.twitter.api import get_tweets_of_user
# from instagram_to_discord.sites.twitter.twitter import twitter_extract_tweet_id, twitter_fetch_content_return_image_urls


if __name__ == "__main__":
    from sys import argv
    userid = argv[1]
    # 非公開鍵垢ユーザはAPIによる取得ができなかった...(これが目的だったのに)
    r = get_tweets_of_user(argv[1])
    # print("result: ", r)
    # urls = twitter_fetch_content_return_image_urls(r)
    # print(f"urls: {urls}")
