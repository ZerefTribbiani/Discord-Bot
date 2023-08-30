import discord
import youtube_dl
from discord.ext import commands


youtube_dl.utils.bug_reports_message = lambda: ''
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}
ytdl_options = {'format': 'bestaudio/best',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
                'cookiefile': 'youtube_cookies.txt'}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['join'])
    async def connect(self, ctx):
        if not ctx.author.voice:
            await ctx.send('You are not in a voice channel')
            return
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url, title=True):
        await self.connect(ctx)
        ctx.voice_client.stop()
        async with ctx.typing():
            with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
                info = ytdl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
                ctx.voice_client.play(source)
                if title:
                    await ctx.send(f'**Playing:** ```{info["title"]}```')

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Paused')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Resumed')

    @commands.command()
    async def baka(self, ctx):
        await self.play(ctx, r'https://www.youtube.com/watch?v=eb1hpiWKDBo', False)

    @commands.command()
    async def banchod(self, ctx):
        await self.play(ctx, r'https://www.youtube.com/watch?v=TU7yY7SaBWA', False)

    @commands.command()
    async def lisa(self, ctx):
        await self.play(ctx, r'https://www.youtube.com/watch?v=V3wjBzlfF8A', False)

    @commands.command()
    async def passion(self, ctx):
        await self.play(ctx, r'https://www.youtube.com/watch?v=ZGg-ox5l5BE', False)

    @commands.command()
    async def pooja(self, ctx):
        await self.play(ctx, r'https://www.youtube.com/watch?v=xg6EBFQT_d8', False)


def setup(bot):
    bot.add_cog(Music(bot))
