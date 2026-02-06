from Bot_Utils.Channels_Commands.Channel_Commands import *

class Backroom_Channel_Commands(Channel_Commands):
    def __init__(self, user, channel):
        super().__init__(user, channel)
        self.commands = [ #ALL CAP COMMANDS
            'CONTACTS'
        ]

    async def process_command(self, message):

        command = message.content.upper() in self.commands
        bot_name = message.content.upper() in Server_Bot_Variables.bot_contacts.keys()

        if not(command or bot_name):
            return
        
        if command:
            if message.content.upper() == 'CONTACTS':
                await self.process_contact()
            
            return

        if bot_name:
            await self.process_bot_name(message.content)
            return

    async def process_contact(self):
        bot_contact_display = 'Contact List:\n\n'
        for bot_name in list(Server_Bot_Variables.bot_contacts.keys()):
            bot_description = Server_Bot_Variables.bot_contacts[bot_name]['description']
            bot_contact_display += f'{bot_name}: {bot_description}\n'
        
        embed = Server_Bot_Functions.create_embed_from_string(None, bot_contact_display)
        await self.channel.send(embed=embed)

    async def process_bot_name(self, bot_name):
        invite_link = Server_Bot_Variables.bot_contacts[bot_name.upper()]['contact']
        message = f'Click link to invite {bot_name}:\n{invite_link}'
        await self.channel.send(message)