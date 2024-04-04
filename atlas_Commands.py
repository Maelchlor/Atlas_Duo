import discord
from discord.ext import commands
from AtDu_System import *
from AtDuo_User import *

intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)
from webhookCommand import *

Atlas_DuoData = {}

@client.command()
async def AddSystem(ctx,MyName,myCall):
    await ctx.send("Placeholder WIP")
    # await ctx.send("Note: this is holding hte at ain temporary storage and is not able to retrieve currently")
    # await ctx.send("at this moment, call backs are not enable. this will be fixed soon, I am testing the calls and setup only")
    # myData = AtDu_System(MyName)
    # myData.CallText = myCall
    # if ctx.attachment:
    #     print(ctx.attachments[0].url)
    #     print(ctx.attachments.count)
    #     myData.UpdateAvatar(ctx.attachments[0].url)
    # Mywebhook = PrepareHooks(ctx)
    # MyTestData = myData.getJSONData()
    # MyTestData["content"] = "I am a test message using the proxy data you submitted. this is only temporary to confirm everything works"
    # Run_WebHook(Mywebhook)
    
@client.command()
async def AddSystemTestOnly(ctx,MyName,myCall):
    await ctx.send("Note: this is holding the information in temporary storage and is not able to retrieve currently")
    await ctx.send("at this moment, call backs are not enable. this will be fixed soon, I am testing the calls and setup only")
    print("creating class")
    myData = AtDu_System()
    myData.author = ctx.author
    myData.Name = MyName
    print("Class created")
    myData.CallText = myCall
    print("CallText created")
    if ctx.message.attachments:
        print(ctx.message.attachments[0].url)
        myData.Image = ctx.message.attachments[0].url
    Mywebhook = await PrepareHooks(ctx)
    print("webhook created")
    MyTestData = myData.getJSONData()
    print("Json Created")
    MyTestData["content"] = "I am a test message using the proxy data you submitted. this is only temporary to confirm everything works"
    print(MyTestData)
    await Run_WebHook(Mywebhook,MyTestData)

@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems")

@client.command()
async def UpdateSystem(ctx):
    await ctx.send("this is a placeholder for updating existing systems")

@client.command()
async def UseAutoProxy(ctx):
    await ctx.send("this is a placeholder for enabling auto proxy")