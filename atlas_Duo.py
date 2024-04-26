import discord
import time
import re
import aiohttp
import asyncio
import json
import requests
#import discord_webhook

#from dhooks import Webhook
#import requests
#from discord_webhook import DiscordWebhook
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from APIKeys import *
from discord import Webhook
from random import randrange
#as I am learning this, a lot of the stuff will be stored here. I am not sharing the apiKey as it is a direct link to the bot on discord. this will only exist on the machine that will be running it or via a direct transfer. it is secure data.

intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)
from TestCommands import *
from AtDu_System import *
from AtDuo_User import *
from atlas_Commands import *
from webhookCommand import *

MyTestHashTable = {}

@client.event 
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("ATLAS DUO is now ready to use!")
    print("------------------------------")

#fixed example of an event handler.
@client.event
async def on_message(message):
    author_id = message.author.id
    guild_id = message.guild.id 
    author = message.author
    user_id = {"_id": author_id}
    if message.author.bot:
        return
    await client.process_commands(message)
    
    await CheckforProxy(message)
    
    
@client.command()
async def Marco(ctx):
    await ctx.send("POLO!")

@client.command()
async def Random(ctx):
    MyRandom = randrange(10)
    await ctx.send("here is a random number: " + str(MyRandom))
    #await ctx.send("You also sent me "+ str(arg))
    if (MyRandom <5):
        await ctx.send("I got less than 5")
    elif(MyRandom == 5):
        await ctx.send("You got exactly 5? lucky!")
    else:
        await ctx.send("greater than 5")

@client.command()
async def Game(ctx):
    MyRandom = randrange(10)
    await ctx.send("I was called by " + str(ctx.author) + ". Test your luck much?")
    if (MyRandom <5):
        await ctx.send("no such luck")
    else:
        await ctx.send("Alright, guess I can do something. maybe.")

#decide what commands to do and how to do. need to figure out delete of lines and cleanup. unable brain operation
   
@client.command()
async def TestEmbed(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                            description="This is an embed that will show you how to build an embed and the differnt components",
                            color =0xFF5733)
    await ctx.send(embed=embed)
    
@client.command()
async def TestDirectMessage(ctx):
    member = ctx.author
    await ctx.send("preparing a test Direct message")
    try:
        await member.send("This is a test message")
        await ctx.send(':white_check_mark: Your Message has been sent')
    except:
        await ctx.send(':x: Member had their dm close, message not sent')


@client.command()
async def TestReact(ctx):
    def check(reaction, user):  # Our check for the reaction
        return user == ctx.message.author  # We check that only the authors reaction counts

    await ctx.send("Please react to the message!")  # Message to react to

    reaction = await client.wait_for("reaction_add", check=check)  # Wait for a reaction
    await ctx.send(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji

@client.command()
async def CreateBubbleWrap(ctx):
    await ctx.send("Here is some bubble wrap")
    await ctx.send("||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop||")

client.run(Botkey)
