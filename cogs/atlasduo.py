import discord
from discord.ext import commands
from AtDu_System import *
from AtDuo_User import *
from webhookCommand import *
from discord.ext.commands import Context
from SQLDatabaseComponents import *

# is this all getting temp stored in the Atlas_DuoData?

class AtlasDuo(commands.Cog, name="atlasduo"):
    def __init__(self, bot):
        self.bot = bot
        self.Atlas_DuoData = {}

    
@commands.hybrid_command()
async def add(ctx,MyName,myCall):
    await AddSystem(ctx,MyName,myCall)
@commands.hybrid_command()
async def Add(ctx,MyName,myCall):
    await AddSystem(ctx,MyName,myCall)
@commands.hybrid_command()
async def Ad(ctx,MyName,myCall):
    await AddSystem(ctx,MyName,myCall)
@commands.hybrid_command()
async def ad(ctx,MyName,myCall):
    await AddSystem(ctx,MyName,myCall)

@commands.hybrid_command()
async def AddSystem(ctx,MyName,myCall):
    if len(MyName) > 32:
        await ctx.send("Discord has a 32 character limit on names. A shorter name is required")
        return
    userData = GetUserData(str(ctx.author.id))
    if userData.rowcount == 0:
        CreateUserData(str(ctx.author.id),str(ctx.author))
    ProxyStatus = CheckIfProxyExists(myCall,MyName,str(ctx.author.id))
    if ProxyStatus['ExistingProxy'] == False:
        if len(ctx.message.attachments) > 0:
            print(str(ctx.message.attachments[0].url))
            CreateProxy(str(ctx.author.id),MyName,str(ctx.message.attachments[0].url),myCall)
        else:
            print("NoImage")
            CreateProxy(str(ctx.author.id),MyName,'',myCall)
        await ctx.send("Your proxy appears to have been created")
    else:
        MyErrorMessage = "Your Proxy called " + str(MyName) + " appears to already exist."
        if ProxyStatus["NameUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Name in Use."
        elif ProxyStatus["CallUsed"] == True:
            MyErrorMessage = MyErrorMessage + " Requested Call in Use."
        await ctx.send(MyErrorMessage)
   
@commands.hybrid_command()
async def Remove(ctx,MyName):
    await RemoveSystem(ctx,MyName)
@commands.hybrid_command()
async def Rm(ctx,MyName):
    await RemoveSystem(ctx,MyName)
@commands.hybrid_command()
async def Del(ctx,MyName):
    await RemoveSystem(ctx,MyName)
@commands.hybrid_command()
async def remove(ctx,MyName):
    await RemoveSystem(ctx,MyName)
@commands.hybrid_command()
async def rm(ctx,MyName):
    await RemoveSystem(ctx,MyName)

#add an optional react stage to this so that the user has the ability to react to confirm
@commands.hybrid_command()
async def RemoveSystem(ctx,MyName):
    ProxyStatus = CheckIfProxyExists('',MyName,str(ctx.author.id))
    if ProxyStatus['ExistingProxy'] == True:
        DeleteProxy(str(ctx.author.id),MyName)
        await ctx.send(MyName + "System has been deleted")
    else:
        await ctx.send("No Matching System is listed under this user")
        
@commands.hybrid_command()
async def ImportSystem(ctx):
    await ctx.send("this is a placeholder for importing systems\nThis is not yet implemented")

@commands.hybrid_command()
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
        print(ProxyStatus)
        print(ProxyStatus['ExistingProxy'] == True)
        print(ProxyStatus["CallUsed"] == False)
        print(ProxyStatus['ExistingProxy'] == True and ProxyStatus["CallUsed"] == False)
        if ProxyStatus['ExistingProxy'] == True and ProxyStatus["CallUsed"] == False:
            UpdateCallText(str(ctx.author.id),MyNewCall,MyName)
            await ctx.send("Requested update has completed")
        elif ProxyStatus['ExistingProxy'] == True and ProxyStatus["CallUsed"] == True:
            await ctx.send("Updated call is in use.")
        elif ProxyStatus['ExistingProxy'] == False:
            await ctx.send("Requested proxy does not exist")
            
@commands.hybrid_command()
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
        print(ProxyStatus)
        print(ProxyStatusupd)
        if ProxyStatus['ExistingProxy'] == True and ProxyStatusupd["ExistingProxy"] == False:
            UpdateDisplayName(str(ctx.author.id),MyCurrentName,MyNewName)
            await ctx.send("Update Completed")
        elif ProxyStatus['ExistingProxy'] == False:
            await ctx.send("Defined system not found")
        elif ProxyStatus['ExistingProxy'] == True and ProxyStatusupd["ExistingProxy"] == True:
            await ctx.send("The new name is already in use")

#throws error when no image is passed
@commands.hybrid_command()
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
            NewUrl = str(ctx.message.attachments[0].url)
            print(ctx.message.attachments[0].url)
        else:
            await ctx.send("no image provided, this will clear existing image")
        ProxyStatus = CheckIfProxyExists('',MyCurrentName,str(ctx.author.id))
        if ProxyStatus['ExistingProxy'] == True:
            UpdateImageURL(str(ctx.author.id),NewUrl,MyCurrentName)
            await ctx.send("Image updated")    
        elif ProxyStatus['ExistingProxy'] == False:
            await ctx.send("Proxy submitted is not found")
        

@commands.hybrid_command()
async def UseAutoProxy(ctx,TargetProxy):
    ProxyStatus = CheckIfProxyExists('',TargetProxy,str(ctx.author.id))
    if ProxyStatus['ExistingProxy'] == True:
        EnableAutoProxy(str(ctx.author.id),TargetProxy)
        await ctx.send("AutoProxy Enabled")
    else:
        await ctx.send("Requested proxy does not exist")


@commands.hybrid_command()
async def StopAutoProxy(ctx):
    DisableAutoProxy(str(ctx.author.id))
    await ctx.send("AutoProxy disabled")

#planned space for checking a message for proxy implementation    
async def CheckforProxy(message):
    AD_ProxyResults = {
        'ProxyFound':False,
        'GUID' : None,
        'WebHooks' : None,
        'autoProxy' :False}
    UserData = getUserAutoProxyState(str(message.author.id))
    if UserData.rowcount == 0:
        pass
    else:
        for row in UserData:
            if row[0] == True:
                print("Autoproxy on, skip some of the checks")
                AD_ProxyResults['ProxyFound'] = True
                AD_ProxyResults['autoProxy'] = True
                AD_ProxyResults['GUID'] = row[1]
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
            if AD_ProxyResults['autoProxy'] == False:
                JSON_Data["content"] = str(message.content[len(AD_ProxyResults["ReplaceText"]):])
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
                        "title" : "ReplyTo:" + RepliedMessage.author.mention,
                        "url" : RepliedMessage.jump_url 
                    }
                ]
            await Run_WebHook(AD_ProxyResults['WebHooks'],JSON_Data)
            await message.delete()

def setup(bot):
    bot.add_cog(AtlasDuoCog(bot))
