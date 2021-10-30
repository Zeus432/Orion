import discord
from discord.ext import commands

from dateutil.relativedelta import relativedelta
import asyncio
import datetime
import json

def load_json(file):
    with open(file, encoding = 'utf-8') as newfile:
        return json.load(newfile)


def write_json(file, contents):
    with open(file, 'w') as newfile:
        json.dump(contents, newfile, ensure_ascii = True, indent = 4)

def get_uptime(bot):
    delta_uptime = relativedelta(datetime.datetime.now(), bot.launch_time)
    days, hours, minutes, seconds = delta_uptime.days, delta_uptime.hours, delta_uptime.minutes, delta_uptime.seconds

    uptimes = {x[0]: x[1] for x in [('day', days), ('hour', hours), ('minute', minutes), ('second', seconds)] if x[1]}
    l = len(uptimes) 

    last = " ".join(value for index, value in enumerate(uptimes.keys()) if index == len(uptimes)-1)

    uptime_string = ", ".join(
        f"{uptimes[value]} {value}{'s' if uptimes[value] > 1 else ''}" for index, value in enumerate(uptimes.keys()) if index != l-1
    )
    uptime_string += f" and {uptimes[last]}" if l > 1 else f"{uptimes[last]}"
    uptime_string += f" {last}{'s' if uptimes[last] > 1 else ''}"
        
    return uptime_string

class CheckAsync(commands.Converter):
    async def isAsync(self, ctx, argument):
        return asyncio.iscoroutinefunction(self)

class Confirm(discord.ui.View):
    def __init__(self, onconfirm: CheckAsync, oncancel: CheckAsync, ontimeout: CheckAsync, timeout: float = 180.0):
        super().__init__(timeout=timeout)
        self.onconfirm = onconfirm
        self.oncancel = oncancel
        self.ontimeout = ontimeout
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.onconfirm(self, button, interaction)
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.oncancel(self, button, interaction)
    
    async def on_timeout(self):
        await self.ontimeout(self)

#async def try_add_reaction(self, emoji: str):
        """Try to add a reaction to the message. """
        #try:
           #await self.message.add_reaction(emoji)
        #except discord.Forbidden:
            #pass

        # Check this later