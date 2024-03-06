import discord
import time
#import requests
from discord.ext import commands
from APIKeys import *
from random import randrange
#as I am learning this, a lot of the stuff will be stored here. I am not sharing the apiKey as it is a direct link to the bot on discord. this will only exist on the machine that will be running it or via a direct transfer. it is secure data.

intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)


@client.event 
async def on__ready():
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
    #print(str(message.content))
    if message.author.bot:
        return
    if message.content.startswith(str.lower("oranges")): 
        await message.channel.send('Here is a new test method!') 
        #print("Least we got here.")
    #if "roxy" in message.content.lower():
        #await message.channel.send('Roxy has been mentioned. Should I get out the martini glasses or prepare for a wave of furries?')
    await client.process_commands(message)
    

@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am ATLAS DUO. I am a bot used for DIDOSDD systems.")
    #myRandom = randrange(5,20)
    #time.sleep(myRandom)
    #await ctx.send("Maybe my first project should be a bit less ambitious, however knowing this family...")
    #await ctx.send("Did you notice the delay? I waited " + str(myRandom) + " seconds to continue" )
    

@client.command()
async def TestMessage1(ctx):
    await ctx.send("This is a test, only a test. breaking everything begins now.")
    await ctx.send("seeing if this sends multiple messages or if I am misunderstanding this.")
    await ctx.send("Purple and pink.")
    
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
async def AddSystem(ctx):
    await ctx.send("this is a placeholder for adding systems")

@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems")

@client.command()
async def UpdateSystem(ctx):
    await ctx.send("this is a placeholder for updating existing systems")

@client.command()
async def UseAutoProxy(ctx):
    await ctx.send("this is a placeholder for enabling auto proxy")

client.run(Botkey)


