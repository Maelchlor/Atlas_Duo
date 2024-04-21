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
    await ctx.send("Placeholder WIP - data will purge after app resets")
    #myData = AtDu_System(MyName,ctx.author,myCall)
    if not ctx.author in Atlas_DuoData:
        Atlas_DuoData[ctx.author] = AtDuo_User(ctx.author)
    print(len(ctx.message.attachments))
    if len(ctx.message.attachments) > 1:
       await ctx.send("I have grabbed the first image submitted")
        #MyReturnCode = Atlas_DuoData[ctx.author].AddProxy(MyName,myCall,ctx.message.attachments[0].url)
    
        
    MyReturnCode = Atlas_DuoData[ctx.author].AddProxy(MyName,myCall,ctx)
    if MyReturnCode == 1:
        await ctx.send("Your proxy appears to have been created")
    else:
        MyErrorMessage = "Your Proxy called " + str(MyName) + " appears to already exist."
        if MyReturnCode & 2 == 2:
            MyErrorMessage = MyErrorMessage + " Requested Name in Use."
        elif MyReturnCode & 4 == 4:
            MyErrorMessage = MyErrorMessage + " Requested Call in Use."
        await ctx.send(MyErrorMessage)
    
    
@client.command()
async def RemoveSystem(ctx,MyName):
    if not ctx.author in Atlas_DuoData:
        Atlas_DuoData[ctx.author] = AtDuo_User(ctx.author)
        await ctx.send("This user has no data, please create items then delete")
        return None
    MyReturnCode = Atlas_DuoData[ctx.author].RemoveProxy(MyName)
    if MyReturnCode["ItemDeleted"] == True:
        await ctx.send("Item Deleted successfully")
    elif MyReturnCode["ItemFound"] == False:
        await ctx.send("Requested proxy not found")
    else:
        await ctx.send("Unknown error has occurred.")
        
    
# @client.command()
# async def AddSystemTestOnly(ctx,MyName,myCall):
#     await ctx.send("Note: this is holding the information in temporary storage and is not able to retrieve currently")
#     await ctx.send("at this moment, call backs are not enable. this will be fixed soon, I am testing the calls and setup only")
#     print("creating class")
#     myData = AtDu_System()
#     myData.author = ctx.author
#     myData.Name = MyName
#     print("Class created")
#     myData.CallText = myCall
#     print("CallText created")
#     if ctx.message.attachments:
#         print(ctx.message.attachments[0].url)
#         myData.Image = ctx.message.attachments[0].url
#     Mywebhook = await PrepareHooks(ctx)
#     print("webhook created")
#     MyTestData = myData.getJSONData()
#     print("Json Created")
#     MyTestData["content"] = "I am a test message using the proxy data you submitted. this is only temporary to confirm everything works"
#     print(MyTestData)
#     await Run_WebHook(Mywebhook,MyTestData)

@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems")

@client.command()
async def UpdateSystem(ctx):
    await ctx.send("this is a placeholder for updating existing systems")

@client.command()
async def UseAutoProxy(ctx):
    await ctx.send("this is a placeholder for enabling auto proxy")

#planned space for checking a message for proxy implementation    
async def CheckforProxy(message):
    #check for autoproxy
    #check for list of prefixes
    #otherwise return as normal
    if message.author in Atlas_DuoData:
        if Atlas_DuoData[message.author].IsAutoProxy == True:
            print(str(message.author) + " has enabled autoproxy")
            Bot_JSON = {}
            Bot_JSON["content"] = "I see Autoproxy attempted. NYI"
            Bot_JSON["username"] = "Atlas_Duo"
            Bot_JSON["avatar_url"] = "https://media.discordapp.net/attachments/1212866248535441469/1213210590412021770/image.png?ex=661054e9&is=65fddfe9&hm=0623351975726152753d694237ac7189ba1c0cd970551f11a96aea5879dfc2b4&=&format=webp&quality=lossless"
            WebHooks = await PrepareHooks(message)
            await Run_WebHook(WebHooks,JSON_Data)
        else:
            #print(message.content)
            for entry in Atlas_DuoData[message.author].Systems:
                if message.content.startswith(entry.CallText):
                    print("we got a possible hit")
                    #await ctx.send("preparing to send using bot, I am not deleting yet as this may false flag as this is early alpha")
                    Bot_JSON = {}
                    Bot_JSON["content"] = "This is an alpha test, I think I saw a call"
                    Bot_JSON["username"] = "Atlas_Duo"
                    Bot_JSON["avatar_url"] = "https://media.discordapp.net/attachments/1212866248535441469/1213210590412021770/image.png?ex=661054e9&is=65fddfe9&hm=0623351975726152753d694237ac7189ba1c0cd970551f11a96aea5879dfc2b4&=&format=webp&quality=lossless"
                    WebHooks = await PrepareHooks(message)
                    await Run_WebHook(WebHooks,Bot_JSON)
                    JSON_Data = entry.getJSONData()
                    JSON_Data["content"] = str(message.content[len(entry.CallText):])
                    RepliedMessage = ''
                    try:
                        print(str(message.reference.message_id))
                        RepliedMessage = await message.channel.fetch_message(message.reference.message_id)
                        print(RepliedMessage.content)
                        
                    except:
                        pass
                    
                    if not RepliedMessage == "":
                        JSON_Data["embeds"] =[
                            {
                                "description" : RepliedMessage.content,
                                "title" : "Jump",
                                "url" : RepliedMessage.jump_url 
                            }
                        ]
                    await Run_WebHook(WebHooks,JSON_Data)