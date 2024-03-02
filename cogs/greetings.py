import discord
from discord.ext import commands

class greetings(commands.cog):
        def __init__(self, client):
            self.client = client 
    #command
    @commands.event 
    async def on__ready():
        await client.change_presence(status=discord.Status.online)
        print("ATLAS DUO is now ready to use!")
        print("------------------------------")
    #event
    @commands.cog.listener()
    async def hello(ctx):
        await ctx.send("Hello! I am ATLAS DUO. I am a bot used for DIDOSDD systems.")
        
def setup(client):
    client.add_cog(greetings(client))