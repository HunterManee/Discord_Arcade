
from Bot_Utils import Server_Bot_Variables
from Bot_Utils import Server_Bot_Functions

async def process_how_to_play(client_response):
    game_id = client_response['game_id']
    display_name = client_response['display_name']
    how_to_play = client_response['content']
    color_code = client_response['color_code']

    location = None
    try:
        location = await Server_Bot_Variables.server_bot.bot.fetch_user(game_id)
    except:
        location =  await Server_Bot_Variables.server_bot.bot.fetch_channel(game_id)
    finally:
        location = location


    embed = Server_Bot_Functions.create_embed_from_string(display_name, how_to_play, color_code)

    if game_id in Server_Bot_Variables.how_to_play_displays.keys():
        await Server_Bot_Variables.how_to_play_displays[game_id].delete()

    message = await location.send(embed=embed)

    Server_Bot_Variables.how_to_play_displays[game_id] = message

async def process_game_list(client_response):
    guild = await Server_Bot_Variables.server_bot.bot.fetch_guild(client_response['guild_id'])
    client_bot = await Server_Bot_Variables.server_bot.bot.fetch_user(client_response['client_bot_id'])
    Server_Bot_Variables.guild_client_bot_dictionary[guild].append(client_bot)
    Server_Bot_Variables.client_bot_game_dictionary[client_bot] = client_response['game_list']
    
    

