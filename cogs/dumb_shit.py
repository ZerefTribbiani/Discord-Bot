from random import choice
from re import sub, search

from discord.ext import commands

import data

class DumbShit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Dumb shit cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        content = sub(r'<:\w*:\d*>', '', message.clean_content)  # Removes emojis
        if search('69|420|666|727', content):
            await message.channel.send('Nice')
        elif self.bot.user in message.mentions:
            await message.channel.send(f'{message.author.mention} {choice(data.swears)}')

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
        await ctx.send(choice(data.yo_mama_jokes))
    
    @commands.command(aliases=['puns'])
    async def pun(self, ctx):
        await ctx.send(choice(data.puns))


async def setup(bot):
    await bot.add_cog(DumbShit(bot))