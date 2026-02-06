from Bot_Utils import Server_Bot_Functions
from Bot_Utils import Server_Bot_Variables


class Channel_Commands:
    def __init__(self, user, channel):
        self.user = user
        self.channel = channel
        self.parent_commands = [
            'MENU'
        ]

    async def process_command(self, message):

        command = message.content.upper() in self.parent_commands
        if not(command):
            return
        
        if command:
            if message.content.upper() == 'MENU':
                await self.process_menu(message.guild)

        return 'success'

    async def process_menu(self, guild):
        menu_display = 'Available Games:\n'

        if guild == None:
            dm_game_list = Server_Bot_Functions.get_games()

            for game_name in dm_game_list:
                menu_display += f'{game_name}\n'

        else:
            
            for client_bot in Server_Bot_Variables.guild_client_bot_dictionary[guild]:
                for game_name in list(Server_Bot_Variables.client_bot_game_dictionary[client_bot]):
                    if game_name is None:
                        continue
                    menu_display += f'{game_name}\n'


        embed = Server_Bot_Functions.create_embed_from_string(None, menu_display)

        if self.channel.id in Server_Bot_Variables.menu_displays.keys():
            await Server_Bot_Variables.menu_displays[self.channel.id].delete()

        message = await self.channel.send(embed=embed)

        Server_Bot_Variables.menu_displays[self.channel.id] = message