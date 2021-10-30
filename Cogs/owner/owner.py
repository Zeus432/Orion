import discord
from discord.ext import commands

from contextlib import redirect_stdout
import traceback
import asyncio
import textwrap
import sys
import io
import os

from .useful import cleanup_code
from Core.Utils import Confirm

class Owner(commands.Cog):
    """ Overall bot related management stuff, or just for abuse commands """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_result = None
    
    async def cog_check(self, ctx: commands.Context):
        result = await self.bot.is_owner(ctx.author)
        if result:
            return True
        raise commands.NotOwner()
    
    @commands.command(name='eval', brief = "Evaluate Code")
    async def _eval(self, ctx: commands.Context, *, body: str):
        """ 
        **Execute asynchronous code.**
        This command wraps code into the body of an async function and then
        calls and awaits it. The bot will respond with anything printed to
        stdout, as well as the return value of the function.

        The code can be within a codeblock, inline code or neither, as long
        as they are not mixed and they are formatted correctly.

        **Environment Variables:**
        `ctx` - command invocation context
        `bot` - bot object
        `channel` - the current channel object
        `author` - command author's member object
        `message` - the command's message object
        `discord` - discord.py library
        `_` - The result of the last dev command.
        """

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = cleanup_code(content = body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
    
    @_eval.error
    async def _eval_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Give me something to eval dumbass, this isn't just for you to flex your eval perms")
        else:
            print(error)
    
    @commands.command(name="shutdown", aliases = ['die','sd','stop'], help = "Shutdown the Bot", brief = "Shutdown")
    async def shutdown(self, ctx: commands.Context):
        # Define some confirm buttons functions
        async def onconfirm(view: discord.ui.View, button: discord.Button, interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return
            await view.message.edit("https://tenor.com/view/nick-fury-mother-damn-it-gone-bye-bye-gif-16387502", view = None)
            try:
                await ctx.message.add_reaction("\U00002705")
            except:
                pass
            view.stop()
            await self.bot.close()

        async def oncancel(view: discord.ui.View, button: discord.Button, interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return
            for item in view.children:
                item.disabled = True
                item.style = discord.ButtonStyle.red if item == button else discord.ButtonStyle.gray 
            await view.message.edit("Cancelled Shutdown...",view = view)
            view.stop()

        async def ontimeout(view: discord.ui.View):
            for item in view.children:
                item.disabled = True
                item.style = discord.ButtonStyle.red if item.label == "Cancel" else discord.ButtonStyle.gray 
            await view.message.edit("Cancelled Shutdown...",view = view)

        view = Confirm(onconfirm, oncancel, ontimeout, 60)
        view.message = await ctx.reply("Are you sure you want to shutdown?", view = view)
    
    @commands.command(brief = "Restart Bot")
    async def restart(self, ctx: commands.Context):
        """ Restart the Bot  """
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)
        message = await ctx.send(f"{self.bot.user} is Restarting")
        try:
            restart_program()
        except:
            await ctx.message.add_reaction("\U000026a0")
            await message.edit('Error I was unable to restart')