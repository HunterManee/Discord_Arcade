from Bot_Utils.Channels_Commands.Channel_Commands import *

class Regular_Channel_Commands(Channel_Commands):
    def __init__(self, user, channel):
        super().__init__(user, channel)
        self.child_commands = [ #ALL CAP COMMANDS

        ]

    async def process_command(self, message):
        outcome = await super().process_command(message)
        if outcome == 'success':
            return

        game_title = message.content in Server_Bot_Functions.get_guild_games(message.guild)

        if not(game_title) :
            return

        if game_title:
            client_bot = Server_Bot_Functions.get_client_bot_for_guild_game(message.guild, message.content)
            server_message = {
                'host_id': message.author.id,
                'game_id': message.author.id,
                'content': message.content
            }
            
            await Server_Bot_Variables.server_bot.send_message_to_client(client_bot, server_message)

