import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=":)", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')
    await load_cogs()

@bot.event
async def on_disconnect():
    print(f'{bot.user} has been disconnected')

@bot.event
async def on_resumed():
    print(f'{bot.user} has resumed session')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    if message.content == ':)':
        await message.channel.send(':)')

    await bot.process_commands(message)

async def load_cogs():
    abs_path = os.path.dirname(__file__)
    rel_path = 'cogs'
    full_path = os.path.join(abs_path, rel_path)
    for file in os.listdir(full_path):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)

