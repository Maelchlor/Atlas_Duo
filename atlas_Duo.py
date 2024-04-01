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
    #author = message.author.locale #not available at this level. will be available as an option for them to select when setting up the app. possibly via DM
    user_id = {"_id": author_id}
    #print(str(message.content))
    if message.author.bot:
        return
    #if re.match('oranges',message.content):
    #   await message.channel.send('Here is a regex test for this word!') 
    #print(str.lower(message.content))
    if str.lower(message.content).startswith("replacemetext"): 
        #print("Least we got here.")
        myVar = message.content
        try:
            print(str(message.reference))
        except:
            print("reference not it")
        
        JSON_Data = {
            "content" : str(message.content[13:]),
            "username" : str(message.author) + "_TestBot",
            "avatar_url" : "https://media.discordapp.net/attachments/1212866248535441469/1213210590412021770/image.png?ex=661054e9&is=65fddfe9&hm=0623351975726152753d694237ac7189ba1c0cd970551f11a96aea5879dfc2b4&=&format=webp&quality=lossless"
        }
        if None == message.reference:
            print("This is not a reply")
        else:
            print("This is a reply")
            #JSON_Data["message_reference"] = message.reference.message_id
     
        print (JSON_Data)
        My_Webhook = await PrepareHooks(message)
        await Run_WebHook(My_Webhook,JSON_Data)
        await message.delete()
        
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
async def AddToTableTest(ctx,Value,MyTestContent):
    await ctx.send("I am adding " + Value + " to the table as a Key. Adding " + MyTestContent + " as its value")
    if ctx.author not in MyTestHashTable:
        MyTestHashTable[ctx.author] = {}
    MyTestHashTable[ctx.author][Value] = MyTestContent
    
@client.command()
async def RetrieveTableTest(ctx,Value):
    if ctx.author not in MyTestHashTable:
        await ctx.send("this user hasn't stored anything")
        return
    if Value not in MyTestHashTable[ctx.author]:
        await ctx.send("This value was not defined")
        return
    await ctx.send("I am Retrieving " + Value + " to the table, it returns " + MyTestHashTable[ctx.author][Value])
    
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
async def CreateClass(ctx):
    Value = 'myClassTest'
    if ctx.author not in MyTestHashTable:
        MyTestHashTable[ctx.author] = {}
    if Value not in MyTestHashTable[ctx.author]:
        MyUserData = AtDuo_User()
        MyUserData.Name = ctx.author
        MyTestHashTable[ctx.author][Value] = MyUserData
        await ctx.send("Data Stored")
        print(MyUserData.Name)
        #print(MyUserData.__MyUUID)



@client.command()
async def TestWebhook(ctx):
    myHook = await PrepareHooks(ctx)
    data = {
    "content" : "Testing a JSON object for this.",
    "username" : "MyTestData"
    }
    await Run_WebHook(myHook,data)

async def PrepareHooks(ctx):
    Iexist = False
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        if webhook.name == 'Atlas Duo WebHook':
            Iexist = True
            myHook = webhook
    if Iexist == False:
        #print("No hook detected, creating")
        await ctx.channel.create_webhook(name='Atlas Duo WebHook')
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            if webhook.name == 'Atlas Duo WebHook':
                myHook = webhook
    return myHook

async def Run_WebHook(Webhook,JSON_Data):
    url = Webhook.url
    result = requests.post(url, json = JSON_Data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    #else:
    #    print("Payload delivered successfully, code {}.".format(result.status_code))

@client.command()
@commands.has_permissions(manage_messages=True)
async def CheckifMod(ctx):
    msg = "This user appears to have manage_messages access: {}".format(ctx.message.author.mention)
    await ctx.send(msg)
 
@CheckifMod.error
async def CheckifMod_error(ctx, error):
    if isinstance(error, CheckFailure):
        msg = "user calling this does not have manage_messages access: {}".format(ctx.message.author.mention)  
        await ctx.send(msg)

client.run(Botkey)