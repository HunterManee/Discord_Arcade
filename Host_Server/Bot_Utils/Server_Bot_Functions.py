import discord

from Bot_Utils import Server_Bot_Variables
from Bot_Utils import Server_Bot_Response_Processing

async def validate_bot(server_bot, bot_info):
    client_bot = await server_bot.fetch_user(bot_info['bot_id'])
    
    for guild in list(Server_Bot_Variables.guild_client_bot_dictionary.keys()):
        for memeber in list(Server_Bot_Variables.guild_client_bot_dictionary[guild]):
            if memeber == client_bot:
                Server_Bot_Variables.client_bot_game_dictionary[client_bot] = bot_info['game_list']
    return client_bot


def get_guild_games(guild):
    total_game_list = []
    for client_bot in Server_Bot_Variables.guild_client_bot_dictionary[guild]:
        total_game_list += Server_Bot_Variables.client_bot_game_dictionary[client_bot]
    return total_game_list

def get_games():
    total_game_list = []
    for game_list in Server_Bot_Variables.client_bot_game_dictionary.values():
        total_game_list += game_list

    return total_game_list

def get_client_bot_for_guild_game(guild, game_title):
    for client_bot in Server_Bot_Variables.guild_client_bot_dictionary[guild]:
        if game_title in Server_Bot_Variables.client_bot_game_dictionary[client_bot]:
            return client_bot
    return None

def get_client_bot_for_game(game_title):
    for client_bot in Server_Bot_Variables.client_bot_game_dictionary.keys():
        if game_title in Server_Bot_Variables.client_bot_game_dictionary[client_bot]:
            return client_bot
    return None

def create_embed_from_string(title = None, display = None, color_code = 'general'):

    if color_code == 'focus':
        embed = discord.Embed(title=title, description=f"```\n{display}\n```", color=discord.Color.og_blurple())
    else:
        embed = discord.Embed(title=title, description=f"```\n{display}\n```", color=discord.Color.dark_purple())
    
    return embed

async def process_response(client_response):
    is_how_to_play = 'How To Play' in client_response['content'] if 'content' in list(client_response.keys()) else False
    is_game_list = 'game_list' in client_response.keys()

    print(f'is_game_list={is_game_list}')
    if is_how_to_play:
        await Server_Bot_Response_Processing.process_how_to_play(client_response)

    if is_game_list:
        await Server_Bot_Response_Processing.process_game_list(client_response)

async def unfocus_messages():
    pass