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
    if len(MyName) > 32:
        await ctx.send("Discord has a 32 character limit on names. A shorter name is required")
        return
    await ctx.send("Placeholder WIP - data will purge after app resets")
    #myData = AtDu_System(MyName,ctx.author,myCall)
    if not ctx.author in Atlas_DuoData:
        Atlas_DuoData[ctx.author] = AtDuo_User(ctx.author)
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
        MyReturnCode = Atlas_DuoData[ctx.author].UpdateProxyCall(MyCurrent,MyNew)
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
        MyReturnCode = Atlas_DuoData[ctx.author].UpdateProxyName(MyCurrent,MyNew)
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
                    
        MyReturnCode = Atlas_DuoData[ctx.author].UpdateProxyImage(MyCurrent,NewUrl)
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
    MyReturnCode = Atlas_DuoData[ctx.author].SetAutoProxy(TargetProxy)
    if MyReturnCode['Updated'] == False:
            if MyReturnCode['ItemFound'] == False:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
    else:
        await ctx.send(str(TargetProxy) + " AutoProxy is now active") 


@client.command()
async def StopAutoProxy(ctx):
    Atlas_DuoData[ctx.author].StopAutoProxy()
    await ctx.send("AutoProxy disabled")

#planned space for checking a message for proxy implementation    
async def CheckforProxy(message):
    #check for autoproxy
    #check for list of prefixes
    #otherwise return as normal
    AD_ProxyResults = {
            'ProxyFound':False,
            'Entry' : None,
            'WebHooks' : None
        }
    if message.author in Atlas_DuoData:
        if Atlas_DuoData[message.author].IsAutoProxy == True:
            print(str(message.author) + " has enabled autoproxy")
            AD_ProxyResults['ProxyFound'] = True
            AD_ProxyResults['WebHooks'] = await PrepareHooks(message)
            AD_ProxyResults['Entry'] = Atlas_DuoData[message.author].AutoProxyTarget
            print("We Got here")
            print(Atlas_DuoData[message.author])
            print(Atlas_DuoData[message.author].AutoProxyTarget.Name)
            print(AD_ProxyResults['Entry'])
            print("We Got here also")
        else:
            for entry in Atlas_DuoData[message.author].Systems:
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
        if Atlas_DuoData[message.author].IsAutoProxy == False:
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