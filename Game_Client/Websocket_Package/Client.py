import random
from Websocket_Package.Websocket import *

from Bot_Utils import Client_Bot_Functions

class Client(Websocket):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.websocket = None

    
    async def start_websocket_client(self):
        asyncio.create_task(self.websocket_client())

    async def websocket_client(self):
        while True:
            try:
                async with websockets.connect(self.WEBSOCKET_URI) as websocket:
                    print(f"Connected to WebSocket server at {self.WEBSOCKET_URI}")
                    self.websocket = websocket
                    
                    # Send bot ID to the server for identification
                    await self.initializeClientConnection()

                    # Listening for messages from the server bot
                    while True:
                        response = await websocket.recv()
                        server_response = json.loads(response)
                        print(f"Received from server bot: {server_response}")
                        message = await Client_Bot_Functions.process_response(server_response)
                        await self.send_message(message)
                        
            except (websockets.ConnectionClosed, OSError) as e:
                print(f"Connection closed with error: {e}. Attempting to reconnect...")
                self.websocket = None
                await asyncio.sleep(random.uniform(1, 5))

    #client -> server (inital)
    async def initializeClientConnection(self):
        message = json.dumps({'bot_id': self.bot.user.id, 'game_list': Client_Bot_Functions.get_game_list()})
        await self.websocket.send(message)  # Send the bot's ID and name

    #client -> server (standard)
    async def send_message(self, message):
        client_message = json.dumps(message)
        await self.websocket.send(client_message)