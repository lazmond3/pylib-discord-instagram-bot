from . import env_check, main, mkdir_notexists

if __name__ == "__main__":
    mkdir_notexists(
        [
            "dumps",
            "dump_videos",
            "dump_videos_instagram",
            "dump_images",
            "dump_images_instagram",
            "dump_json_instagram",
            "dump_json",
        ]
    )
    env_check()
    main()
