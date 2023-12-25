import discord
from discord.ext import commands

token="MTE4ODIwMTAyNjA1MDg3MTMwNg.GXA9BO.CxJXOOzNWmiOuklI5E6YvlYePMz3weA0EhwzO4"

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@client.event
async def on_ready(): 
    print("I am ready")


@client.command()
async def test(ctx):
    await ctx.send("It works")

@client.command(pass_context=True)
async def play(ctx):
    if(ctx.author.voice):
        channel=ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Pls join a Voicechannel to use this command")
        # await ctx.send(ctx.message.content) Testing for getting input besides -play 
        # message=ctx.message.content 
        # message=message.split(" ")
        # await ctx.send(message[1])
        
    



client.run(token)
