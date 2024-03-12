import discord
from discord.ext import commands
intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)



@client.command()
async def ImportedMessage(ctx):
    await ctx.send("This is a test, only a test. breaking everything begins now.")
    await ctx.send("This was called from a separate file from the first file")
    await ctx.send("This is going to see what happens")
    
    
