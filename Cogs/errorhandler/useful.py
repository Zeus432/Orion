import discord
from discord.ext import commands

import logging
import traceback

logger = logging.getLogger('OrionLog')

async def send_error(bot: commands.Bot, ctx: commands.Context, error):
    embed = discord.Embed(title = "Command Error!", description = f"This error has been forwarded to the bot developer and will be fixed soon.\nIn the meanwhile please refrain from trying to recreate this error unnecessarily.\n\n```py\n{error}```", colour = discord.Colour(0x2F3136))
    embed.set_footer(text = "Spamming errored commands will get you blacklisted!", icon_url = ctx.author.avatar or ctx.author.default_avatar)
    await ctx.reply(embed = embed)

    # Log in Error Logs
    traceback_error = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    logger.error(f"{traceback_error}")

    # Now Log in Error Channel
    embed.description = f"{ctx.message.content}"

    embed.add_field(name = "Author:", value = f"{ctx.author.mention}\n (`{ctx.author.id}`)")
    if ctx.guild:
        embed.add_field(name = "Channel:", value = f"{ctx.channel.mention}\n (`{ctx.channel.id}`)")
        embed.add_field(name = "Guild:", value = f"**{ctx.guild}**\n (`{ctx.guild.id}`)")
    else:
        embed.add_field(name = "Dm Channel:", value = f"<#{ctx.channel.id}>\n (`{ctx.channel.id}`)")
    embed.add_field(name = "Message ID:", value = f"`{ctx.message.id}`")
    embed.add_field(name = "\u200b", value = f"**[\U0001f517 Jump to Error]({ctx.message.jump_url})**")

    # Split Error if it's longer than 1900k Charecter to fit discord limits
    split_error, final_error = "", []
    for line in traceback_error.split('\n'):
        if len(split_error + line) < 1900:
            split_error += f"\n{line}"

        else:
            final_error.append(split_error)
            split_error = ""
    final_error.append(split_error)

    error_channel = bot.get_channel(bot.config["errorchannel"])
    await error_channel.send(embed = embed)
    for e in final_error:
        await error_channel.send(f"```py\n{e}```")
