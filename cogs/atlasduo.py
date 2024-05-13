import discord
from discord.ext import commands
from AtDu_System import *
from AtDuo_User import *
from webhookCommand import *
from discord.ext.commands import Context

# is this all getting temp stored in the Atlas_DuoData?

class AtlasDuo(commands.Cog, name="atlasduo"):
    def __init__(self, bot):
        self.bot = bot
        self.Atlas_DuoData = {}

    @commands.hybrid_command()
    async def AddSystem(self, ctx: Context, MyName, myCall):
        if len(MyName) > 32:
            await ctx.send("Discord has a 32 character limit on names. A shorter name is required")
            return
        await ctx.send("Placeholder WIP - data will purge after app resets")
        if ctx.author not in self.Atlas_DuoData:
            self.Atlas_DuoData[ctx.author] = AtDuo_User(ctx.author)
        if len(ctx.message.attachments) > 1:
            await ctx.send("I have grabbed the first image submitted")
        
        MyReturnCode = self.Atlas_DuoData[ctx.author].AddProxy(MyName, myCall, ctx)
        if MyReturnCode == 1:
            await ctx.send("Your proxy appears to have been created")
        else:
            MyErrorMessage = f"Your Proxy called {MyName} appears to already exist."
            if MyReturnCode & 2 == 2:
                MyErrorMessage += " Requested Name in Use."
            elif MyReturnCode & 4 == 4:
                MyErrorMessage += " Requested Call in Use."
            await ctx.send(MyErrorMessage)

    @commands.hybrid_command()
    async def RemoveSystem(self, ctx: Context, MyName):
        if ctx.author not in self.Atlas_DuoData:
            self.Atlas_DuoData[ctx.author] = AtDuo_User(ctx.author)
            await ctx.send("This user has no data, please create items then delete")
            return
        MyReturnCode = self.Atlas_DuoData[ctx.author].RemoveProxy(MyName)
        if MyReturnCode["ItemDeleted"]:
            await ctx.send("Item Deleted successfully")
        elif not MyReturnCode["ItemFound"]:
            await ctx.send("Requested proxy not found")
        else:
            await ctx.send("Unknown error has occurred.")

    @commands.hybrid_command()
    async def ImportSystem(self, ctx: Context):
        await ctx.send("this is a placeholder for importing systems\nThis is not yet implemented")

    @commands.hybrid_command()
    async def UpdateSystemCall(self, ctx: Context, MyCurrent=None, MyNew=None):
        if MyCurrent is None or MyNew is None:
            await ctx.send("Error: The target System or new Call was not provided")
            return
        
        MyReturnCode = self.Atlas_DuoData[ctx.author].UpdateProxyCall(MyCurrent, MyNew)
        if not MyReturnCode['Updated']:
            if not MyReturnCode['ItemFound']:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(f"{MyCurrent} has had the call text updated")

    @commands.hybrid_command()
    async def UpdateSystemName(self, ctx: Context, MyCurrent=None, MyNew=None):
        if MyCurrent is None or MyNew is None:
            await ctx.send("Error: The target System or new name was not provided")
            return
        
        MyReturnCode = self.Atlas_DuoData[ctx.author].UpdateProxyName(MyCurrent, MyNew)
        if not MyReturnCode['Updated']:
            if not MyReturnCode['ItemFound']:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(f"{MyCurrent} has been renamed to {MyNew}")

    @commands.hybrid_command()
    async def UpdateSystemImage(self, ctx: Context, MyCurrent=None):
        if MyCurrent is None:
            await ctx.send("Error: The target System was not provided")
            return
        
        NewUrl = ''
        if len(ctx.message.attachments) > 0:
            NewUrl = ctx.message.attachments[0].url

        MyReturnCode = self.Atlas_DuoData[ctx.author].UpdateProxyImage(MyCurrent, NewUrl)
        if not MyReturnCode['Updated']:
            if not MyReturnCode['ItemFound']:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(f"{MyCurrent} the new image has been applied")

    @commands.hybrid_command()
    async def UseAutoProxy(self, ctx: Context, TargetProxy):
        MyReturnCode = self.Atlas_DuoData[ctx.author].SetAutoProxy(TargetProxy)
        if not MyReturnCode['Updated']:
            if not MyReturnCode['ItemFound']:
                await ctx.send("Passed system was not found")
            else:
                await ctx.send("An unknown error has occurred")
        else:
            await ctx.send(f"{TargetProxy} AutoProxy is now active")

    @commands.hybrid_command()
    async def StopAutoProxy(self, ctx: Context):
        self.Atlas_DuoData[ctx.author].StopAutoProxy()
        await ctx.send("AutoProxy disabled")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        AD_ProxyResults = {
            'ProxyFound': False,
            'Entry': None,
            'WebHooks': None
        }

        if message.author in self.Atlas_DuoData:
            if self.Atlas_DuoData[message.author].IsAutoProxy:
                AD_ProxyResults['ProxyFound'] = True
                AD_ProxyResults['WebHooks'] = await self.PrepareHooks(message)
                AD_ProxyResults['Entry'] = self.Atlas_DuoData[message.author].AutoProxyTarget
            else:
                for entry in self.Atlas_DuoData[message.author].Systems:
                    if message.content.startswith(entry.CallText):
                        AD_ProxyResults['ProxyFound'] = True
                        AD_ProxyResults['WebHooks'] = await self.PrepareHooks(message)
                        AD_ProxyResults['Entry'] = entry

        if AD_ProxyResults['ProxyFound']:
            JSON_Data = AD_ProxyResults['Entry'].getJSONData()
            if not self.Atlas_DuoData[message.author].IsAutoProxy:
                JSON_Data["content"] = message.content[len(AD_ProxyResults['Entry'].CallText):]
            else:
                JSON_Data["content"] = message.content

            RepliedMessage = ''
            try:
                RepliedMessage = await message.channel.fetch_message(message.reference.message_id)
            except:
                pass

            if RepliedMessage:
                JSON_Data["embeds"] = [
                    {
                        "description": RepliedMessage.content,
                        "title": "Jump",
                        "url": RepliedMessage.jump_url
                    }
                ]
            await Run_WebHook(AD_ProxyResults['WebHooks'], JSON_Data)
            await message.delete()

    async def PrepareHooks(self, message):
        # Implement this function based on your logic for preparing webhooks
        pass

def setup(bot):
    bot.add_cog(AtlasDuoCog(bot))
