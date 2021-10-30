import discord
from discord.ext import commands

import os
import time
import inspect
from datetime import datetime

from Core.Utils import get_uptime
from .useful import ghlinkbutton

class BotStuff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command(name = "ping", help = "View the ping of the bot", brief = "Take a wild guess")
    async def ping(self, ctx: commands.Context):
        async with ctx.typing():
            start = time.perf_counter()
            msg = await ctx.send(f"Pinging...")
            end = time.perf_counter()
        typing_ping = (end - start) * 1000

        embed = discord.Embed(description = f"```yaml\nTyping: {round(typing_ping, 1)} ms\nWebsocket: {round(self.bot.latency*1000)} ms```", colour = discord.Colour(0x2F3136))

        await msg.edit(content = "Pong \U0001f3d3", embed = embed)
    
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command(name='uptime', brief = "Bot Uptime")
    async def uptime(self, ctx: commands.Context):
        """Gets the uptime of the bot"""
        uptime_string = get_uptime(self.bot)
        await ctx.channel.send(f'{self.bot.user} has been up for {uptime_string}.\nSince <t:{round(self.bot.launch_ts)}>')
    
    @commands.command(brief = "Get Command Source")
    async def source(self, ctx: commands.Context, *, command: str = None):
        """Displays my full source code or for a specific command.
        To display the source code of a subcommand you can separate it by
        periods, e.g. permissions.add for the add subcommand of the permissions command
        or by spaces.
        """
        source_url = self.bot.config['github']['source']
        branch = self.bot.config['github']['branch']

        view = discord.ui.View()
        embed = discord.Embed(colour = self.bot.colour)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar or ctx.author.default_avatar)

        if command is None:
            embed.title = "Here's the entire repo"
            return await ctx.send(embed = embed, view = ghlinkbutton(view, source_url))

        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            command = command.replace('.', ' ')
            obj = self.bot.get_command(command)
            if obj is None:
                return await ctx.send('Could not find command.')

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        location = os.path.relpath(filename).replace('\\', '/')

        embed.title = f"Here's the source for `{command}`"
        final_url = f'{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'

        await ctx.send(embed = embed, view = ghlinkbutton(view, final_url))