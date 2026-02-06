import discord
from discord.ext import commands
from env import env

from Websocket_Package.Client import *

from Bot_Utils import Client_Bot_Variables

#Set Up Permissions
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.dm_messages = True
#https://discordpy.readthedocs.io/en/latest/intents.html

#Create instance of ClientBot
bot = commands.Bot(command_prefix='∆', intents=intents)
client_bot = Client(bot)

@bot.event
async def on_ready():
    print('ClientBot is ONLINE...')
    print('=======================================')
    Client_Bot_Variables.client_bot = client_bot
    await client_bot.start_websocket_client()

bot.run(env.CLIENT_TOKEN)

