from Bot_Utils import Client_Bot_Variables
from Bot_Utils import Client_Bot_Response_Processing

def get_game_list():
    game_list = list(Client_Bot_Variables.game_dictionary.keys())
    return game_list

async def process_response(server_response):
    content = server_response['content']
    
    is_game_title = content in list(Client_Bot_Variables.game_dictionary.keys())
    need_game_list = content == 'game_list'

    if is_game_title:
        return await Client_Bot_Response_Processing.process_game_title(server_response)
    
    if need_game_list:
        return Client_Bot_Response_Processing.process_game_list(server_response)
        