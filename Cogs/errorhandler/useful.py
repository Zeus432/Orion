import discord
from discord.ext import commands

import logging
import traceback

logger = logging.getLogger('OrionLog')

async def send_error(bot: commands.Bot, ctx, error):
    embed = discord.Embed(title = "Command Error!", description = f"This error has been forwarded to the bot developer and will be fixed soon.\nIn the meanwhile please refrain from trying to recreate this error unnecessarily.\n\n```py\n{error}```", colour = discord.Colour(0x2F3136))
    embed.set_footer(text = "Spamming errored commands will get you blacklisted!", icon_url = ctx.author.avatar or ctx.author.default_avatar)
    await ctx.reply(embed = embed)
    traceback_error = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    logger.error(f"{traceback_error}")

