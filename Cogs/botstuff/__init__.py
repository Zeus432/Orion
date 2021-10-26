from discord.ext import commands
from .botstuff import BotStuff

def setup(bot: commands.Bot):
    bot.add_cog(BotStuff(bot))