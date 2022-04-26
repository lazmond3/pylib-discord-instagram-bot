from instagram_to_discord.sites.twitter.api import (
    get_following_list,
    get_tweets_of_user,
)

# from instagram_to_discord.sites.twitter.twitter import twitter_extract_tweet_id, twitter_fetch_content_return_image_urls


if __name__ == "__main__":
    from sys import argv

    userid = argv[1]
    r = get_following_list(screen_name=argv[1], cursor=argv[2])
