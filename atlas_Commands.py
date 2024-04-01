import discord
from discord.ext import commands

intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)

Atlas_DuoData = {}

@client.command()
async def AddSystem(ctx):
    await ctx.send("Placeholder text")
    #await ctx.send("this will temporarily save the system passed. it will delete as the load state is not enabled")
    #if ctx.author not in Atlas_DuoData:
    #    Atlas_DuoData[ctx.author] = {}
    #Atlas_DuoData[ctx.author][Value] = MyTestContent

@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems")

@client.command()
async def UpdateSystem(ctx):
    await ctx.send("this is a placeholder for updating existing systems")

@client.command()
async def UseAutoProxy(ctx):
    await ctx.send("this is a placeholder for enabling auto proxy")