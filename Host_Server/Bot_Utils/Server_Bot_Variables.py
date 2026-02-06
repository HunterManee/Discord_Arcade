server_bot = None

arcade_channels = list() #channel
backroom_channels = list() #backroom

bot_contacts = {
    #client_bot.name : invite link
    'CLIENTBOT' : { #Bot name must be uppercase
        'contact' : 'https://discord.com/oauth2/authorize?client_id=1291795942626033684&permissions=8&integration_type=0&scope=bot',
        'description' : 'Demo Games'
        }
}

guild_client_bot_dictionary = dict() #guild : list(client_bot)
client_bot_game_dictionary = dict() #client_bot : game_list

menu_displays = dict() #channel_id : message *1 menu per channel
how_to_play_displays = dict() #game_id : message *1 how_to_play per game_id (user/channel id)*

player_game_displays = dict() #user_id : {display_name : message}
#display_name = channel.name or game.title
player_focused_display = dict() #user_id : message
