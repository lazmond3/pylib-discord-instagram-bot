from instagram_to_discord.sites.twitter.api import get_following_list

if __name__ == "__main__":
    from sys import argv

    userid = argv[1]
    r = get_following_list(screen_name=argv[1], cursor=argv[2])
