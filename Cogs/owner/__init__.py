from discord.ext import commands
from .owner import Owner

def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))