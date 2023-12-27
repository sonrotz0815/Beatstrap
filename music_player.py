from ast import alias
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import asyncio

class Beatstrap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False
        self.loop=False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

     #searching the item on youtube
    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return{'source':item, 'title':title}
        search = VideosSearch(item, limit=1)
        return{'source':search.result()["result"][0]["link"], 'title':search.result()["result"][0]["title"]}

    async def play_next(self):
        if len(self.music_queue) > 0 or self.loop:
            self.is_playing = True
            #get the first url
            m_url = self.music_queue[0][0]['source']
            print(m_url)
            #remove the first element as you are currently playing it
            if(self.loop==False):
                self.music_queue.pop(0)
            
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        print("balls")
        if len(self.music_queue) > 0 or self.loop:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("You are in no Voice Channel cunt")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            
            if(self.loop==False):
                self.music_queue.pop(0)
            
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
            print("Yarak")
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="plays song matching with url or Keyword")
    async def play(self, ctx, *args):
        message=ctx.message.channel
        channel = discord.utils.get(ctx.guild.channels, name="╠🎶music🎶")
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("Connect to a Voice Channel cunt")
            return
        if self.is_paused:
            self.vc.resume()
        else:
            if(channel==message):
                song = self.search_yt(query)
                
                if type(song) == type(True):
                    await ctx.send("Invalid Input --> Gib was anderes ein Oglum")
                else:
                    if self.is_playing:
                        await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** added to the queue")  
                    else:
                        await ctx.send(f"**'{song['title']}'** added to the queue")  
                    self.music_queue.append([song, voice_channel])
                    
                    if self.is_playing == False:
                        await self.play_music(ctx)

            else:
                await ctx.send("You are in the wrong Channel cunt")
    
    @commands.command(name="pause", aliases=["resume","r"], help="Pauses/Resumes current song")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="skips currently playing song")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="shows the queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(f"```queue:\n{retval}```")
        else:
            await ctx.send("The fucking queue is empty")

    @commands.command(name="clear", aliases=["c", "bin"], help="emptys the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("The queue is clean now cunt")

    @commands.command(name="looped", aliases=["l","infinite"], help="Loops the currently playing song")
    async def looped(self,ctx):
        if(self.loop):
            self.loop=False
            await ctx.send("You are not in a fucking loop anymore")
        else:
            self.loop=True
            await ctx.send("You are now in a fucking loop")
    