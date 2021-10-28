from discord.ext import commands
from .errorhandler import ErrorHandler

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))