from Bot_Utils import Client_Bot_Variables

async def process_game_title(server_response):

    host_id = server_response['host_id']
    game_id = server_response['game_id']
    game_title = server_response['content']

    try:
        await Client_Bot_Variables.client_bot.bot.fetch_user(host_id)
    except:
        return 'LogicERROR: Invalid Host Id'

    try:
        user = await Client_Bot_Variables.client_bot.bot.fetch_user(game_id)
    except:
        user = None

    try:
        channel = await Client_Bot_Variables.client_bot.bot.fetch_channel(game_id)
    except:
        channel = None

    if user == None and channel == None:
        #Results from id is not a real id or client bot is not a memeber of the server
        return 'LogicERROR: Invalid Game ID'
    
    game_instance = Client_Bot_Variables.game_dictionary[game_title](host_id)
    display_name = None
    #user
    if not(user == None):
        display_name = game_title

        if len(Client_Bot_Variables.active_games) == 0:
            Client_Bot_Variables.active_games[game_id] = { display_name : game_instance}

        elif (len(Client_Bot_Variables.active_games) > 0 and
                game_id in list(Client_Bot_Variables.active_games.keys())):
                user_game_dictionary = Client_Bot_Variables.active_games[game_id]
                user_game_list = list(user_game_dictionary.keys())

                #game_title is in user game list
                if display_name in user_game_list:
                    message = {
                        'game_id' : game_id,
                        'display_name' : display_name,
                        'content' : game_instance.process_how_to_play(),
                        'color_code' : 'focus'
                    }
                    return message
                
                Client_Bot_Variables.active_games[game_id] = { display_name : game_instance}

        else: #if active games length is greater than 0 and game_id not in active_game keys
            Client_Bot_Variables.active_games[game_id] = { display_name : game_instance}

    #channel
    elif not(channel == None):
        if game_id in list(Client_Bot_Variables.active_games.keys()):
            del Client_Bot_Variables.active_games[game_id]

        display_name = f'{channel.name} | {game_title}'
        Client_Bot_Variables.active_games[game_id] = { display_name : Client_Bot_Variables.game_dictionary[game_title](host_id) }

    message = {
        'game_id' : game_id,
        'display_name' : display_name,
        'content' : game_instance.process_how_to_play(),
        'color_code' : 'general'
    }

    return message

def process_game_list(server_response):
    return {
                'guild_id' : server_response['guild_id'],
                'client_bot_id' : server_response['client_bot_id'],
                'game_list' : list(Client_Bot_Variables.game_dictionary.keys()) 
            }

    
