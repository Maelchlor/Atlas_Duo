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

#I already see a complete rewrite in this area. you already learned some new stuff
#the memory method used is able to work for a small scale, we will need to think larger. this will ultimately have to query the sql.


@client.command()
async def AddSystem(ctx,MyName,myCall):
    if len(MyName) > 32:
        await ctx.send("Discord has a 32 character limit on names. A shorter name is required")
        return
    await ctx.send("Placeholder WIP - data will purge after app resets")
    #myData = AtDu_System(MyName,ctx.author,myCall)
    
    if not ctx.author.id in Atlas_DuoData:
        Atlas_DuoData[ctx.author.id] = AtDuo_User(ctx.author,ctx.author.id)
    if len(ctx.message.attachments) > 1:
       await ctx.send("I have grabbed the first image submitted")
        #MyReturnCode = Atlas_DuoData[ctx.author].AddProxy(MyName,myCall,ctx.message.attachments[0].url)
    
        
    MyReturnCode = Atlas_DuoData[ctx.author.id].AddProxy(MyName,myCall,ctx)
    
    if MyReturnCode["Success"] == True:
        await ctx.send("Your proxy appears to have been created")
    else:
        MyErrorMessage = "Your Proxy called " + str(MyName) + " appears to already exist."
        if MyReturnCode["NameUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Name in Use."
        elif MyReturnCode["CallUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Call in Use."
        await ctx.send(MyErrorMessage)
    
    
@client.command()
async def RemoveSystem(ctx,MyName):
    if not ctx.author.id in Atlas_DuoData:
        Atlas_DuoData[ctx.author.id] = AtDuo_User(ctx.author,ctx.author.id)
        await ctx.send("This user has no data, please create items then delete")
        return None
    MyReturnCode = Atlas_DuoData[ctx.author.id].RemoveProxy(MyName)
    if MyReturnCode["ItemDeleted"] == True:
        await ctx.send("Item Deleted successfully")
    elif MyReturnCode["ItemFound"] == False:
        await ctx.send("Requested proxy not found")
    else:
        await ctx.send("Unknown error has occurred.")
        
@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems\nThis is not yet implemented")

@client.command()
async def UpdateSystemCall(ctx,MyCurrent=None,MyNew=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyCurrent == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if MyNew == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The System's new Call was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        MyReturnCode = Atlas_DuoData[ctx.author.id].UpdateProxyCall(MyCurrent,MyNew)
        print(MyReturnCode)
        if MyReturnCode['Updated'] == False:
            if MyReturnCode['ItemFound'] == False:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(str(MyCurrent) + " has had the call text updated")
            
@client.command()
async def UpdateSystemName(ctx,MyCurrent=None,MyNew=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyCurrent == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if MyNew == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The System's new name was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        MyReturnCode = Atlas_DuoData[ctx.author.id].UpdateProxyName(MyCurrent,MyNew)
        print(MyReturnCode)
        if MyReturnCode['Updated'] == False:
            if MyReturnCode['ItemFound'] == False:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(str(MyCurrent) + " has been renamed to " + str(MyNew))

@client.command()
async def UpdateSystemImage(ctx,MyCurrent=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyCurrent == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        NewURL = ''
        if len(ctx.message.attachments) > 0:
            NewUrl = ctx.message.attachments[0].url
                    
        MyReturnCode = Atlas_DuoData[ctx.author.id].UpdateProxyImage(MyCurrent,NewUrl)
        print(MyReturnCode)
        if MyReturnCode['Updated'] == False:
            if MyReturnCode['ItemFound'] == False:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(str(MyCurrent) + " the new image has been applied")

@client.command()
async def UseAutoProxy(ctx,TargetProxy):
    MyReturnCode = Atlas_DuoData[ctx.author.id].SetAutoProxy(TargetProxy)
    if MyReturnCode['Updated'] == False:
            if MyReturnCode['ItemFound'] == False:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
    else:
        await ctx.send(str(TargetProxy) + " AutoProxy is now active") 


@client.command()
async def StopAutoProxy(ctx):
    Atlas_DuoData[ctx.author.id].StopAutoProxy()
    await ctx.send("AutoProxy disabled")

#planned space for checking a message for proxy implementation    
async def CheckforProxy(message):
    AD_ProxyResults = {
            'ProxyFound':False,
            'Entry' : None,
            'WebHooks' : None
        }
    if message.author.id in Atlas_DuoData:
        if Atlas_DuoData[message.author.id].IsAutoProxy == True:
            print(str(message.author.id) + " has enabled autoproxy")
            AD_ProxyResults['ProxyFound'] = True
            AD_ProxyResults['WebHooks'] = await PrepareHooks(message)
            AD_ProxyResults['Entry'] = Atlas_DuoData[message.author.id].AutoProxyTarget
            print("We Got here")
            print(Atlas_DuoData[message.author.id])
            print(Atlas_DuoData[message.author.id].AutoProxyTarget.Name)
            print(AD_ProxyResults['Entry'])
            print("We Got here also")
        else:
            for entry in Atlas_DuoData[message.author.id].Systems:
                if message.content.startswith(entry.CallText):
                    print("we got a possible hit")
                    AD_ProxyResults['ProxyFound'] = True
                    AD_ProxyResults['WebHooks'] = await PrepareHooks(message)
                    AD_ProxyResults['Entry'] = entry
                    
    if AD_ProxyResults['ProxyFound'] == True:
        print("here we go again")
        print(AD_ProxyResults['Entry'])
        print("Did we write?")
        
        JSON_Data = AD_ProxyResults['Entry'].getJSONData()
        if Atlas_DuoData[message.author.id].IsAutoProxy == False:
            JSON_Data["content"] = str(message.content[len(AD_ProxyResults['Entry'].CallText):])
        else:
            JSON_Data["content"] = str(message.content)
        RepliedMessage = ''
        try:
            print(str(message.reference.message_id))
            RepliedMessage = await message.channel.fetch_message(message.reference.message_id)
            print(RepliedMessage.content)
            
        except:
            pass
        #it uses a username, link with the reply message, and then the actual replied message
        if not RepliedMessage == "":
            JSON_Data["embeds"] =[
                {
                    "description" : RepliedMessage.content,
                    "title" : "Jump",
                    "url" : RepliedMessage.jump_url 
                }
            ]
        await Run_WebHook(AD_ProxyResults['WebHooks'],JSON_Data)
        await message.delete()