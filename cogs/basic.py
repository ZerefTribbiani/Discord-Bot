import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipe = {guild.id: {channel.id: None for channel in guild.text_channels} for guild in bot.guilds}
        self.stop_spam = {guild.id: {channel.id: None for channel in guild.text_channels} for guild in bot.guilds}
        print('Basic cog loaded')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.snipe[guild.id] = {channel.id: None for channel in guild.text_channels}

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del self.snipe[guild.id]

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.snipe[message.guild.id][message.channel.id] = message


    @commands.command()
    async def snipe(self, ctx):
        message = self.snipe[ctx.guild.id][ctx.channel.id]
        if message:
            embed = discord.Embed(description=message.content, colour=message.author.colour, timestamp=message.created_at)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send("There's nothing to snipe")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def spam(self, ctx, spam_count: int, *, content):
        for _ in range(spam_count):
            if self.stop_spam[ctx.guild.id][ctx.channel.id]:
                self.stop_spam[ctx.guild.id][ctx.channel.id] = False
                break
            else:
                await ctx.send(content)

    @commands.command(name='stopspam')
    async def stop_spam(self, ctx):
        self.stop_spam[ctx.guild.id][ctx.channel.id] = True

    @commands.command(aliases=['delete'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, clr_count: int = 1):
        users = ctx.message.mentions
        if users:
            deleted = await ctx.channel.purge(limit=clr_count, check=lambda msg: msg.author in users, before=ctx.message)
        else:
            deleted = await ctx.channel.purge(limit=clr_count, before=ctx.message)
        deleted = len(deleted)
        await ctx.message.delete()
        await ctx.send(f'{deleted} messages have been deleted :)', delete_after=5)

    @commands.command(name='clearmy', aliases=['deletemy'])
    async def clear_my(self, ctx, clr_count: int = 1):
        deleted = await ctx.channel.purge(limit=clr_count, check=lambda msg: msg.author==ctx.author, before=ctx.message)
        await ctx.message.delete()
        await ctx.send(f'{deleted} messages have been deleted :)', delete_after=5)


async def setup(bot):
    await bot.add_cog(Basic(bot))