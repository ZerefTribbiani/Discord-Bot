import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.ytdl_options = {'format': 'bestaudio',
                             'noplaylist': 'True'}
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnected_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = None

        print('Music cog loaded')

    def search_yt(self, search_query):
        with YoutubeDL(self.ytdl_options) as ytdl:
            try:
                info = ytdl.extract_info('ytsearch:{search_query}', download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if self.music_queue:
            self.is_playing = True
            url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(url, **self.ffmpeg_options), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if self.music_queue:
            self.is_playing = True
            url = self.music_queue[0][0]['source']

            if not self.vc or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

async def setup(bot):
    await bot.add_cog(Music(bot))