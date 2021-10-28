import discord
from discord.ext import commands

import logging

from .useful import send_error

class ErrorHandler(commands.Cog, name = "ErrorHandler"):
    """ Module for Global Error Handling and Logging"""

    def __init__(self, bot):
        self.bot = bot
        logger = logging.getLogger('OrionLog')
        logger.info("Error Handler Logged in")
        self.logger = logger

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""
        if hasattr(ctx.command, 'on_error'):
            return
        senderr = None
        cmd = self.bot.get_command(ctx.invoked_with)

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return


        ignored = (commands.CommandNotFound, commands.NoPrivateMessage, commands.ExpectedClosingQuoteError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            return await ctx.reply(f'This command is disabled.')

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send_help(ctx.command)
        
        elif isinstance(error, commands.NotOwner):
            return await ctx.reply(f"These are Bot Owner only commands and I don't see you on the list \U0001f440", mention_author = False)

        elif isinstance(error, commands.CheckFailure):
            return await ctx.reply(f"Missing Permissions!")
        
        elif isinstance(error, commands.GuildNotFound):
            return await ctx.send(f'Could not find guild: `{error.argument}`')

        elif isinstance(error, commands.BadArgument):
            return await ctx.send_help(ctx.command)
        
        elif isinstance(error, commands.errors.CommandOnCooldown):
            return await ctx.reply(f'Whoa chill with the spam boi, Try again in {round(error.retry_after, 2)} seconds')
        
        elif isinstance(error, commands.MissingPermissions):
            if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.permissions_for(ctx.channel.guild.me).send_messages:
                senderror = True
            else: pass
        else:
            senderror = True

        if senderror:
            await send_error(bot = self.bot, ctx = ctx, error = error)