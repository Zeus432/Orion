import discord
from discord.ext import commands

import logging
import aiohttp
import pathlib
import asyncio

from Core.Utils import *
from Core.settings import INITIAL_EXTENSIONS

config = load_json('Core/config.json')
TOKEN = config['TOKEN']

rootdir = pathlib.Path(__file__).parent.resolve()

# Loggers help keep your console from being flooded with Errors, you can instead send them to a file which you can check later
logger = logging.getLogger('Log')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'{rootdir}/Core/Orion.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Orion(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix = commands.when_mentioned_or(*config['prefix']),  intents = discord.Intents.all(), activity = discord.Game(name="Waking Up"), status=discord.Status.idle, case_insensitive=True, **kwargs)
        self.description = config['description']

        # Load Initial Extensions
        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}\n{type(e).__name__}: {e}')
    
    async def start(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)
    
    async def close(self):
        await self.session.close()
        await super().close()
    
    async def on_ready(self):
        print(f'\nLogged in as {self.user} (ID: {self.user.id})')
        print(f'Guilds: {len(self.guilds)}')
        print(f'Large Guilds: {sum(g.large for g in self.guilds)}')
        print(f'Chunked Guilds: {sum(g.chunked for g in self.guilds)}')
        print(f'Members: {len(list(self.get_all_members()))}')
        print(f'Channels: {len([1 for x in self.get_all_channels()])}')
        print(f'Message Cache Size: {len(self.cached_messages)}\n')
        await asyncio.sleep(10)
        await self.change_presence(status=discord.Status.idle, activity = discord.Activity(type=discord.ActivityType.watching, name=f"for @{self.user.name} help"))
        logger.info("Orion is Online!")
    
    def run(self):
        super().run(TOKEN, reconnect=True)

if __name__ == "__main__":
    orion = Orion()
    orion.run()