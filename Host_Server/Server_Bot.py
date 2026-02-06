import discord
from discord.ext import commands
from env import env

from Websocket_Package.Server import *

from Bot_Utils import Server_Bot_Variables
from Bot_Utils import Server_Bot_Commands

#Set Up Permissions
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.dm_messages = True
intents.presences = True  # Required to track presence (online/offline) updates
#https://discordpy.readthedocs.io/en/latest/intents.html


#Create instance of ServerBot
bot = commands.Bot(command_prefix='!', intents=intents)
server_bot = Server(bot)

# Server Interaction ##############################################
@bot.event
async def on_ready():
    '''
    Waking up the ServerBot for Discord
    
    ServerBot searches for a through all the channels it has access to for the following channel names:
        -arcade
        -backroom
    '''

    print('ServerBot is ONLINE...')
    print('=======================================')
    Server_Bot_Variables.server_bot = server_bot

    for guild in bot.guilds:
        Server_Bot_Variables.guild_client_bot_dictionary[guild] = list()
        for member in guild.members:
            if member.name.upper() in list(Server_Bot_Variables.bot_contacts.keys()):
                
                Server_Bot_Variables.guild_client_bot_dictionary[guild].append(member)

        # Search through all channels in the guild
        for channel in guild.channels:
            if channel.name == 'arcade':
                Server_Bot_Variables.arcade_channels.append(channel)
                continue
            
            if channel.name == 'backroom':
                Server_Bot_Variables.backroom_channels.append(channel)

    await server_bot.start_websocket_server()

# Member Interaction ##############################################
@bot.event
async def on_member_join(member):
    guild = member.guild
    #if the memeber joining member is apart of bot_contacts
    client_bot = member if member.name.upper() in list(Server_Bot_Variables.bot_contacts.keys()) else None
    if client_bot is None:
        return
    
    server_message = {
        'guild_id' : guild.id,
        'client_bot_id': client_bot.id,
        'content' : 'game_list'
    }

    await server_bot.send_message_to_client(client_bot, server_message)

@bot.event
async def on_presence_update(before, after):

    if before.status == after.status:
        return
    
    client_bot_name = after.name.split('#')[0]

    client_bot = after if client_bot_name.upper() in list(Server_Bot_Variables.bot_contacts.keys()) else None
    if client_bot == None:
        return

    if client_bot.status == discord.Status.offline:
        if client_bot in Server_Bot_Variables.guild_client_bot_dictionary[client_bot.guild]:
            Server_Bot_Variables.client_bot_game_dictionary[client_bot] = list()


@bot.event
async def on_member_remove(member):
    guild = member.guild
    # Check if the guild exists in the game dictionary
    if guild in Server_Bot_Variables.guild_client_bot_dictionary:
        # Delete the entry for the member if it exists
        if member in Server_Bot_Variables.guild_client_bot_dictionary[guild]:
            Server_Bot_Variables.client_bot_game_dictionary[member] = list()

            print(f'Removed {member.name} from game dictionary in {guild.name}.')


# Channel Interaction #############################################
@bot.event
async def on_guild_channel_create(channel):

    #A channel named arcade has been created
    if channel.name == 'arcade':       
        Server_Bot_Variables.arcade_channels.append(channel)
        return
    
    #A channel named backroom has been created
    if channel.name == 'backroom':
        Server_Bot_Variables.backroom_channels.append(channel)
        return

@bot.event
async def on_guild_channel_update(before, after):
    if before.name == after.name:
        return

    #If the channel name changed to arcade
    if after.name == 'arcade':
        #If the channel is already in the active game channels
        if after in Server_Bot_Variables.arcade_channels:
            return
        #If the channel isn't already an active game channel then add it
        Server_Bot_Variables.arcade_channels.append(after)
    
    #If the arcade has a how to play already in it
    if after.id in list(Server_Bot_Variables.how_to_play_displays.keys()):
        message = Server_Bot_Variables.how_to_play_displays[after.id]
        embed = message.embeds[0]
        embed.title = after.name + embed.title[len(before.name):]
        await message.edit(embed=embed)
        



    if after.name == 'backroom':
        Server_Bot_Variables.backroom_channels.append(after)
    elif before.name == 'backroom':
        Server_Bot_Variables.backroom_channels.remove(before)

@bot.event
async def on_guild_channel_delete(channel):

    if channel.name == 'backroom':
        Server_Bot_Variables.backroom_channels.remove(channel)
        return

    #If the channel is not in the active game channels
    if channel not in Server_Bot_Variables.arcade_channels:
        return

    #Deleted channel from active game channels
    Server_Bot_Variables.arcade_channels.remove(channel)


   
@bot.event
async def on_message(message):
    user = message.author
    try:
        #If this bot is sending a message
        if bot.user == user:
            return
        
        if isinstance(message.channel, discord.DMChannel):
            await Server_Bot_Commands.DM_Channel_Commands(user, message.channel).process_command(message)
            return

        if isinstance(message.channel, discord.TextChannel):

            #If the message is being sent from an arcade channel
            if message.channel in Server_Bot_Variables.arcade_channels:
                await Server_Bot_Commands.Arcade_Channel_Commands(user, message.channel).process_command(message)
                return
            
            #If the message is being sent from a backroom channel 
            if message.channel in Server_Bot_Variables.backroom_channels:
                await Server_Bot_Commands.Backroom_Channel_Commands(user, message.channel).process_command(message)
                return

            #If the message is being set from a regualar channel
            await Server_Bot_Commands.Regular_Channel_Commands(user, message.channel).process_command(message)
            return
        
    except discord.Forbidden as e:
        print(f'discord: {e}')
        return

bot.run(env.SERVER_TOKEN)
