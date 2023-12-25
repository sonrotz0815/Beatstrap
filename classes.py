import discord 
from discord.ext import commands
from requests import get
from youtube_dl import YoutubeDL




class music_cog(commands.Cog):
    def _init_(self,bot):
        self.bot=bot 

        self.is_playing=False
        self.is_paused=False

        self.music_queue=[]
        self.YDL_OPTIONS={'formart':'bestaudio','noplaylist':'True'}
        self.FFMPEG_OPTIONS={'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}

        self.vc=None


    def search_yt(self,item):
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    get(item) 
                    print(item)
                except:
                    video = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                else:
                    video = ydl.extract_info(item, download=False)

            return video
    

    def play_next(self):
        if len(self.music_queue)>0:
            self.is_playing=True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e : self.play_next()) 

        else:
            self.is_playing=False

    async def play_music(self, ctx):
    
        if len(self.music_queue)>0:
            self.is_playing=True
            m_url=self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():  
                self.vc = await self.music_queue[0][1].connect()

                if self.vc==None:
                    await ctx.send("You are not in a Voice Channel you cunt")
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url), **self.FFMPEG_OPTIONS, after=lambda e : self.play_next())
        else:
            self.is_playing=False 
                

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        channel = discord.utils.get(ctx.guild.channels, name="╠🎶music🎶")
        query=" ".join(args)
        # channel = discord.utils.get(client.get_all_channels(), id=781490216334524419)
        voicechannel= ctx.author.voice.channel
        
        if voicechannel is None:
            await ctx.send("You are not Connected to a voice Channel cunt")
        elif ctx.message.channel==channel:
            song=self.search_yt(query)
            
            if type(song)== type(True):
                await ctx.send("Song isnt working cunt, try another keyword")
            
            else:
                await ctx.send("Your song is now playing")
                self.music_queue.append([song,voicechannel])

                if self.is_playing == False:
                    await self.play_music(ctx)
        
        else:
            await ctx.send("You are not in the music channel cunt")
    
    @commands.command(name="pause/resume", aliases=["pause, resume, go, more, weiter"])
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing=False
            self.is_paused=True
            self.vc.paus
        elif self.is_paused:
            self.is_playing=True
            self.is_paused=False
            self.vc.resume()
    
    @commands.command(name="skip", aliases=['s'])
    async def skip(self,ctx,*args):
        if self.vc != None and self.vc:
            self.vc.stop
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q","playlist"])
    async def queue(self, ctx, *args):
        listqueue=""

        for i in range (0, len(self.music_queue)):
            if i>4: i=len(self.music_queue)
            if i<=4:
                listqueue+=self.music_queue[i][0]['title']+"\n"

            if listqueue!="":
                await ctx.send(listqueue)
            else:
                await ctx.send("Queue is empty you cunt")
    
    @commands.command(name="clear")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue=[]
        await ctx.send("I cleared your fucking Queue")
    

