from dataclasses import dataclass
from typing import Dict


@dataclass
class DiscordMemoClient:
    last_url_instagram: Dict[str, str]
    is_twitter_last: bool
