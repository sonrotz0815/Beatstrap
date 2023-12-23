import discord
from discord.ext import commands

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@client.event
async def on_ready(): 
    print("I am ready")


@client.command()
async def test(ctx):
    await ctx.send("It works")

client.run('MTE4ODIwMTAyNjA1MDg3MTMwNg.GXA9BO.CxJXOOzNWmiOuklI5E6YvlYePMz3weA0EhwzO4')
