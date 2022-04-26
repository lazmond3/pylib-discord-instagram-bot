from instagram_to_discord.sites.twitter.api import get_sumatome

if __name__ == "__main__":
    from sys import argv

    tweetid = argv[1]
    r = get_sumatome(tweetid)
    print("result: ", r)
