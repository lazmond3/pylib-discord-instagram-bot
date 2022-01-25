from dataclasses import dataclass
from typing import Dict
import discord


@dataclass
class DiscordMemoClient:
    last_url_instagram: Dict[discord.TextChannel, str]
    last_url_twitter: Dict[discord.TextChannel, str]
    is_twitter_last: bool
