import discord
from discord.ext import commands

import time

from Core.Utils import get_uptime

class BotStuff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name = "ping", help = "View the ping of the bot", brief = "Take a wild guess")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        async with ctx.typing():
            start = time.perf_counter()
            msg = await ctx.send(f"Pinging...")
            end = time.perf_counter()
        typing_ping = (end - start) * 1000

        embed = discord.Embed(description = f"```yaml\nTyping: {round(typing_ping, 1)} ms\nWebsocket: {round(self.bot.latency*1000)} ms```", colour = discord.Colour(0x2F3136))

        await msg.edit(content = "Pong \U0001f3d3", embed = embed)
    
    @commands.command(name='uptime', brief = "Bot Uptime")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def uptime(self, ctx: commands.Context):
        """Gets the uptime of the bot"""
        uptime_string = get_uptime(self.bot)
        await ctx.channel.send(f'{self.bot.user} has been up for {uptime_string}.\nSince <t:{round(self.bot.launch_ts)}>')