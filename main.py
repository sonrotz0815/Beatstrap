import discord
import asyncio
from discord.ext import commands
from music_player import Beatstrap

token="MTE4ODIwMTAyNjA1MDg3MTMwNg.GXA9BO.CxJXOOzNWmiOuklI5E6YvlYePMz3weA0EhwzO4"

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

@client.event
async def on_ready(): 
    print("I am ready")


async def main():
    async with client:
        await client.add_cog(Beatstrap(client))
        await client.start(token)


asyncio.run(main())
