import random
import re

from discord.ext import commands

import idfk


class DumbShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yomama')
    async def yo_mama(self, ctx):
        await ctx.send(random.choice(idfk.yo_mama_jokes))


def setup(bot):
    bot.add_cog(DumbShit(bot))
