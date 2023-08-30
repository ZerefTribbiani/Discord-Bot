import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import idfk

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=':)', intents=discord.Intents.all())

# variables made global in functions
guilds_deleted = {}
stop_spam = False


@bot.event
async def on_ready():
    global guilds_deleted
    guilds_deleted = {guild.id: {channel.id: None for channel in guild.text_channels} for guild in bot.guilds}
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content == ':)':
        await message.channel.send(':)')

    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    guilds_deleted[message.guild.id][message.channel.id] = message


@bot.command()
async def stop(ctx):
    global stop_spam
    stop_spam = True
    await ctx.message.delete(delay=2)


@bot.command()
@commands.has_permissions(manage_guild=True)
async def spam(ctx, times: int, *, content):
    """This SPAMS"""
    global stop_spam
    if stop_spam:
        stop_spam = False

    for _ in range(times):
        if stop_spam:
            stop_spam = False
            return
        await ctx.send(content)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, times: int = 1):
    users = ctx.message.mentions
    if users:
        deleted = 0
        await ctx.message.delete()
        async for message in ctx.channel.history(limit=None, before=ctx.message):
            if message.author in users:
                await message.delete()
                deleted += 1
                if deleted == times:
                    break
    else:
        deleted = await ctx.channel.purge(limit=times, before=ctx.message)
        deleted = len(deleted)
    await ctx.message.delete(delay=2)
    await ctx.send(f'{deleted} messages have been deleted :)', delete_after=5)


@bot.command(name='clearmy')
async def clear_my(ctx, times: int = 1):
    deleted = 0
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.author:
            await message.delete()
            deleted += 1
            if deleted == times:
                break
    await ctx.send(f'{deleted} messages have been deleted :)', delete_after=5)


@bot.command()
async def snipe(ctx):
    message = guilds_deleted[ctx.guild.id][ctx.channel.id]
    if message:
        author = message.author
        content = message.content
        created = message.created_at
        footer = idfk.TimeDelta(datetime.utcnow() - created).display()
        embed = discord.Embed(description=content, colour=discord.Colour(0x00FF00))
        embed.set_author(name=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
    else:
        await ctx.send("There's nothing to snipe")


for file in os.listdir('D:\Code\Python\Projects\DiscordBot\cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)
