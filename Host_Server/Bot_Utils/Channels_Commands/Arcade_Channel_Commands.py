from Bot_Utils.Channels_Commands.Channel_Commands import *

class Arcade_Channel_Commands(Channel_Commands):
    def __init__(self, user, channel):
        super().__init__(user, channel)
        self.child_commands = [ #ALL CAP COMMANDS
            'BEGIN'
        ]

    async def process_command(self, message):
        outcome = await super().process_command(message)
        if outcome == 'success':
            return
        
        game_title = message.content in Server_Bot_Functions.get_guild_games(message.guild)
        command = message.content.upper() in self.child_commands

        if not(game_title or command):
            return
        
        if game_title:
            client_bot = Server_Bot_Functions.get_client_bot_for_guild_game(message.guild, message.content)
            server_message = {
                'host_id': message.author.id,
                'game_id': message.channel.id,
                'content': message.content
            }
            
            await Server_Bot_Variables.server_bot.send_message_to_client(client_bot, server_message)
            return

        if command:
            if message.content.upper() == 'BEGIN':
                how_to_play_display = Server_Bot_Variables.how_to_play_displays[message.channel.id]
                embed = how_to_play_display.embeds[0]
                embed_title = embed.title
                


                return