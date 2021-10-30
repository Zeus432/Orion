import discord
from discord.ext import commands

def ghlinkbutton(view: discord.ui.View, link: str) -> discord.ui.View:
    view.add_item(discord.ui.Button(label = "Source", emoji = "<:Github:896348887185510440>", style = discord.ButtonStyle.link, url = link))
    return view