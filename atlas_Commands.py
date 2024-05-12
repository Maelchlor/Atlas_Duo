import discord

from discord.ext import commands
from AtDu_System import *
from AtDuo_User import *
from SQLDatabaseComponents import *

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
    userData = GetUserData(str(ctx.author.id))
    if userData.rowcount == 0:
        CreateUserData(ctx.author.id,ctx.author)
    ProxyStatus = CheckIfProxyExists(myCall,MyName,str(ctx.author.id))
    if ProxyStatus['ExistingProxy'] == False:
        if len(ctx.message.attachments) > 1:
            CreateProxy(str(ctx.author.id),MyName,'',myCall)
        else:
            CreateProxy(str(ctx.author.id),MyName,'ctx.message.attachments[0].url',myCall)
        await ctx.send("Your proxy appears to have been created")
    else:
        MyErrorMessage = "Your Proxy called " + str(MyName) + " appears to already exist."
        if ProxyStatus["NameUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Name in Use."
        elif ProxyStatus["CallUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Call in Use."
        await ctx.send(MyErrorMessage)
    
#add an optional react stage to this so that the user has the ability to react to confirm
@client.command()
async def RemoveSystem(ctx,MyName):
    ProxyStatus = CheckIfProxyExists('',MyName,str(ctx.author.id))
    if ProxyStatus['ExistingProxy'] == True:
        DeleteProxy(ctx.author.id,MyName)
        ctx.send(MyName + "System has been deleted")
    else:
        ctx.send("No Matching System is listed under this user")
        
@client.command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems\nThis is not yet implemented")

@client.command()
async def UpdateSystemCall(ctx,MyName=None,MyNewCall=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyName == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if MyNewCall == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The System's new Call was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        ProxyStatus = CheckIfProxyExists(MyNewCall,MyName,str(ctx.author.id))
        if ProxyStatus['ExistingProxy'] == True & ProxyStatus["CallUsed"] == False:
            UpdateCallText(ctx.author.id,MyNewCall,MyName)
            ctx.send("Requested update has completed")
        elif ProxyStatus['ExistingProxy'] == True & ProxyStatus["CallUsed"] == True:
            ctx.send("Updated call is in use.")
        elif ProxyStatus['ExistingProxy'] == False:
            ctx.send("Requested proxy does not exist")
            
@client.command()
async def UpdateSystemName(ctx,MyCurrentName=None,MyNewName=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyCurrentName == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if MyNewName == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The System's new name was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        ProxyStatus = CheckIfProxyExists('',MyCurrentName,str(ctx.author.id))
        ProxyStatusupd = CheckIfProxyExists('',MyNewName,str(ctx.author.id))
        if ProxyStatus['ExistingProxy'] == True & ProxyStatusupd["ExistingProxy"] == False:
            UpdateDisplayName(ctx.author.id,MyCurrentName,MyNewName)
        elif ProxyStatus['ExistingProxy'] == False:
            ctx.send("Defined system not found")
        elif ProxyStatus['ExistingProxy'] == True & ProxyStatusupd["ExistingProxy"] == True:
            ctx.send("The new name is already in use")

@client.command()
async def UpdateSystemImage(ctx,MyCurrentName=None):
    ErrorState = {}
    ErrorState["hasError"] = False
    ErrorState["Message"]  = ""
    if MyCurrentName == None:
        ErrorState["hasError"] = True
        ErrorState["Message"] = ErrorState["Message"] + "The target System was not provided"
    if ErrorState["hasError"] == True:
        await ctx.send("Error: " +str(ErrorState["Message"]))
        return
    else:
        NewURL = ''
        if len(ctx.message.attachments) > 0:
            NewUrl = ctx.message.attachments[0].url
        else:
            ctx.send("no image provided, this will clear existing image")
        ProxyStatus = CheckIfProxyExists('',MyCurrentName,ctx.author.id)
        if ProxyStatus['ExistingProxy'] == True:
            UpdateImageURL(str(ctx.author.id),NewURL,MyCurrentName)
            ctx.send("Image updated")    
        elif ProxyStatus['ExistingProxy'] == False:
            ctx.send("Proxy submitted is not found")
        

@client.command()
async def UseAutoProxy(ctx,TargetProxy):
    ProxyStatus = CheckIfProxyExists('',TargetProxy,ctx.author.id)
    if ProxyStatus['ExistingProxy'] == True:
        EnableAutoProxy(str(ctx.author.id),TargetProxy)
        ctx.send("AutoProxy Enabled")
    else:
        ctx.send("Requested proxy does not exist")


@client.command()
async def StopAutoProxy(ctx):
    DisableAutoProxy(str(ctx.author.id))
    await ctx.send("AutoProxy disabled")

#planned space for checking a message for proxy implementation    
async def CheckforProxy(message):
    AD_ProxyResults = {
        'ProxyFound':False,
        'GUID' : None,
        'WebHooks' : None
    }
    UserData = getUserAutoProxyState(str(message.author.id))
    if UserData.rowcount == 0:
        print("no user data")
    else:
        for row in UserData:
            if row[0] == True:
                print("Autoproxy on, skip some of the checks")
                AD_ProxyResults['ProxyFound'] = True
                AD_ProxyResults['GUID'] = UserData[1]
        if AD_ProxyResults['ProxyFound'] == False:
            PrefixList = GetUserProxyPrefix(str(message.author.id))
            for row in PrefixList:
                if message.content.startswith(row[0]):
                    print("we found the proxy")
                    AD_ProxyResults['ProxyFound'] = True
                    AD_ProxyResults['GUID'] = row[1]
        
        if AD_ProxyResults['ProxyFound'] == True:
            print("We got a proxy confirmed")
            ADuo_ProxyData = getSpecificProxy(AD_ProxyResults['GUID'])
            AD_ProxyResults['WebHooks'] = await PrepareHooks(message)
            JSON_Data = {}
            for row in ADuo_ProxyData:
                JSON_Data["username"] = row[5]
                JSON_Data["avatar_url"] = row[6]
                AD_ProxyResults["ReplaceText"] = row[4]
            
            JSON_Data["content"] = str(message.content[len(AD_ProxyResults["ReplaceText"]):])
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
                        "title" : "ReplyTo:" + RepliedMessage.author.mention,
                        "url" : RepliedMessage.jump_url 
                    }
                ]
            await Run_WebHook(AD_ProxyResults['WebHooks'],JSON_Data)
            #await message.delete()