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

    #all commands have to be in the cog :)

    @commands.hybrid_command(
        name="add",
        description="Add a new system to the Atlas Duo Database"
    )
    async def add(ctx:Context, MyName, myCall):
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


    #add an optional react stage to this so that the user has the ability to react to confirm
    @commands.hybrid_command(
        name="remove",
        description="Remove a system from the Atlas Duo Database",
        aliases=["delete", "del", "rm"]
    )
    async def RemoveSystem(ctx:Context, MyName) -> None:
        ProxyStatus = CheckIfProxyExists('',MyName,str(ctx.author.id))
        if ProxyStatus['ExistingProxy'] == True:
            DeleteProxy(str(ctx.author.id),MyName)
            await ctx.send(MyName + "System has been deleted")
        else:
            await ctx.send("No Matching System is listed under this user")

    @commands.hybrid_command(
        name="importSystem",
        description="Import a system from the Atlas Duo Database",
    )
    async def ImportSystem(ctx) -> None:
        await ctx.send("this is a placeholder for importing systems\nThis is not yet implemented")

    @commands.hybrid_command(
        name="update_call",
        description="Update the call sign of a system",
        aliases=["updatecall", "uc"]
    )
    async def UpdateSystemCall(ctx: Context, MyName=None, MyNewCall=None):
        ErrorState = {"hasError": False, "Message": ""}
        if MyName is None:
            ErrorState["hasError"] = True
            ErrorState["Message"] += "The target System was not provided"
        if MyNewCall is None:
            ErrorState["hasError"] = True
            ErrorState["Message"] += "The System's new Call was not provided"
        if ErrorState["hasError"]:
            await ctx.send("Error: " + str(ErrorState["Message"]))
            return
        else:
            ProxyStatus = CheckIfProxyExists(MyNewCall, MyName, str(ctx.author.id))
            if ProxyStatus['ExistingProxy'] and not ProxyStatus["CallUsed"]:
                UpdateCallText(str(ctx.author.id), MyNewCall, MyName)
                await ctx.send("Requested update has completed")
            elif ProxyStatus['ExistingProxy'] and ProxyStatus["CallUsed"]:
                await ctx.send("Updated call is in use.")
            else:
                await ctx.send("Requested proxy does not exist")


    @commands.hybrid_command(
        name="update_name",
        description="Update the name of a system",
        aliases=["updatename", "un"]
    )
    async def UpdateSystemName(ctx: Context, MyCurrentName=None, MyNewName=None):
        ErrorState = {"hasError": False, "Message": ""}
        if MyCurrentName is None:
            ErrorState["hasError"] = True
            ErrorState["Message"] += "The target System was not provided"
        if MyNewName is None:
            ErrorState["hasError"] = True
            ErrorState["Message"] += "The System's new name was not provided"
        if ErrorState["hasError"]:
            await ctx.send("Error: " + str(ErrorState["Message"]))
            return
        else:
            ProxyStatus = CheckIfProxyExists('', MyCurrentName, str(ctx.author.id))
            ProxyStatusupd = CheckIfProxyExists('', MyNewName, str(ctx.author.id))
            if ProxyStatus['ExistingProxy'] and not ProxyStatusupd["ExistingProxy"]:
                UpdateDisplayName(str(ctx.author.id), MyCurrentName, MyNewName)
                await ctx.send("Update Completed")
            elif not ProxyStatus['ExistingProxy']:
                await ctx.send("Defined system not found")
            else:
                await ctx.send("The new name is already in use")


    @commands.hybrid_command(
        name="update_image",
        description="Update the image of a system",
        aliases=["updateimage", "ui"]
    )
    async def UpdateSystemImage(ctx: Context, MyCurrentName=None):
        ErrorState = {"hasError": False, "Message": ""}
        if MyCurrentName is None:
            ErrorState["hasError"] = True
            ErrorState["Message"] += "The target System was not provided"
        if ErrorState["hasError"]:
            await ctx.send("Error: " + str(ErrorState["Message"]))
            return
        else:
            NewUrl = ''
            if len(ctx.message.attachments) > 0:
                NewUrl = str(ctx.message.attachments[0].url)
            else:
                await ctx.send("No image provided, this will clear existing image")
            ProxyStatus = CheckIfProxyExists('', MyCurrentName, str(ctx.author.id))
            if ProxyStatus['ExistingProxy']:
                UpdateImageURL(str(ctx.author.id), NewUrl, MyCurrentName)
                await ctx.send("Image updated")
            else:
                await ctx.send("Proxy submitted is not found")


    @commands.hybrid_command(
        name="use_autoproxy",
        description="Enable AutoProxy for a specific system",
        aliases=["enableautoproxy", "uap"]
    )
    async def UseAutoProxy(ctx: Context, TargetProxy):
        ProxyStatus = CheckIfProxyExists('', TargetProxy, str(ctx.author.id))
        if ProxyStatus['ExistingProxy']:
            EnableAutoProxy(str(ctx.author.id), TargetProxy)
            await ctx.send("AutoProxy Enabled")
        else:
            await ctx.send("Requested proxy does not exist")


    @commands.hybrid_command(
        name="stop_autoproxy",
        description="Disable AutoProxy",
        aliases=["disableautoproxy", "sap"]
    )
    async def StopAutoProxy(ctx: Context):
        DisableAutoProxy(str(ctx.author.id))
        await ctx.send("AutoProxy disabled")


    # Planned space for checking a message for proxy implementation    
    async def CheckforProxy(message):
        AD_ProxyResults = {
            'ProxyFound': False,
            'GUID': None,
            'WebHooks': None,
            'autoProxy': False
        }
        UserData = getUserAutoProxyState(str(message.author.id))
        if UserData.rowcount == 0:
            pass
        else:
            for row in UserData:
                if row[0]:
                    AD_ProxyResults['ProxyFound'] = True
                    AD_ProxyResults['autoProxy'] = True
                    AD_ProxyResults['GUID'] = row[1]
            if not AD_ProxyResults['ProxyFound']:
                PrefixList = GetUserProxyPrefix(str(message.author.id))
                for row in PrefixList:
                    if message.content.startswith(row[0]):
                        AD_ProxyResults['ProxyFound'] = True
                        AD_ProxyResults['GUID'] = row[1]

            if AD_ProxyResults['ProxyFound']:
                ADuo_ProxyData = getSpecificProxy(AD_ProxyResults['GUID'])
                AD_ProxyResults['WebHooks'] = await PrepareHooks(message)
                JSON_Data = {}
                for row in ADuo_ProxyData:
                    JSON_Data["username"] = row[5]
                    JSON_Data["avatar_url"] = row[6]
                    AD_ProxyResults["ReplaceText"] = row[4]
                if not AD_ProxyResults['autoProxy']:
                    JSON_Data["content"] = str(message.content[len(AD_ProxyResults["ReplaceText"]):])
                else:
                    JSON_Data["content"] = str(message.content)
                RepliedMessage = ''
                try:
                    RepliedMessage = await message.channel.fetch_message(message.reference.message_id)
                except:
                    pass
                if RepliedMessage:
                    JSON_Data["embeds"] = [
                        {
                            "description": RepliedMessage.content,
                            "title": "ReplyTo:" + RepliedMessage.author.mention,
                            "url": RepliedMessage.jump_url
                        }
                    ]
                await Run_WebHook(AD_ProxyResults['WebHooks'], JSON_Data)
                await message.delete()

def setup(bot):
    bot.add_cog(AtlasDuoCog(bot))
