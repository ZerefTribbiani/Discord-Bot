import random
import re

from discord.ext import commands

import idfk


class DumbShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return

        content = re.sub(r'<:\w*:\d*>', '', message.clean_content)  # Removes emojis
        if re.search('69|420|666|727', content):
            await message.channel.send('Nice')
        elif self.bot.user in message.mentions:
            await message.channel.send(f'{message.author.mention} {random.choice(idfk.swears)}')

        # if message.author.id in {617052195535192081, 814509133691879454}:
        #    await message.channel.send('Your mom')

    @commands.command()
    async def ligma(self, ctx):
        await ctx.send('Balls')

    @commands.command(aliases=['sukma'])
    async def sugma(self, ctx):
        await ctx.send('Dick')

    @commands.command(name='yomama')
    async def yo_mama(self, ctx):
        await ctx.send(random.choice(idfk.yo_mama_jokes))


def setup(bot):
    bot.add_cog(DumbShit(bot))
