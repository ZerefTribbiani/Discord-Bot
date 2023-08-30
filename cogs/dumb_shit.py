from random import choice
from re import sub, search

from discord.ext import commands

import data

class DumbShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Dumb shit cog loaded')

    @commands.command(name='yomama')
    async def yo_mama(self, ctx):
        await ctx.send(choice(data.yo_mama_jokes))
    
    @commands.command(aliases=['puns'])
    async def pun(self, ctx):
        await ctx.send(choice(data.puns))


async def setup(bot):
    await bot.add_cog(DumbShit(bot))
