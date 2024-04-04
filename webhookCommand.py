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

intents = discord.Intents.default() 
intents.message_content = True 
intents.messages = True 
intents.guilds = True
client = commands.Bot(command_prefix = ['!','ad!','$'], intents=intents)

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