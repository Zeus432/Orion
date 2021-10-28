import discord
import time
from discord.ext import commands

class BotStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "ping", help = "View the ping of the bot", brief = "Take a wild guess")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def ping(self, ctx):
        start = time.perf_counter()
        msg = await ctx.send(f"Pinging \U0001f3d3")
        await ctx.author.trigger_typing()
        end = time.perf_counter()
        typing_ping = (end - start) * 1000

        await msg.edit(content = f"```yaml\nTyping: {round(typing_ping, 1)} ms\nWebsocket: {round(self.bot.latency*1000)} ms```")