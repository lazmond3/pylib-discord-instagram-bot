import discord

def create_ask_embed(
    question: str, 
    answer: str,
    url: str
):
    description = f"""Q.{question}\n\nA. {answer}"""
    embed = discord.Embed(
        title=f"koba",
        description=description,
        url=url,
        color=discord.Color.green(),
    )
    embed.set_author(
        name="koba31okm",
        url="https://twitter.com/koba31okm",
        icon_url="https://pbs.twimg.com/profile_images/1372691769469460486/9Ug_QMow_400x400.jpg",
    )
    return embed
