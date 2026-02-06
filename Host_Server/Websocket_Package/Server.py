from Websocket_Package.Websocket import *

from Bot_Utils import Server_Bot_Functions

class Server(Websocket):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.clients = dict()

    # Start WebSocket server
    async def start_websocket_server(self):
        server = await websockets.serve(self.handle_client, self.HOST, self.PORT)
        print(f"Server bot WebSocket server started on {self.WEBSOCKET_URI}")
        await server.wait_closed()  # This keeps the server running

    # Handle incoming client connections
    async def handle_client(self, websocket, path):
        try:
            # First receive the bot's initial identification message
            initial_message = await websocket.recv()
            bot_info = json.loads(initial_message)
            
            client_bot = await Server_Bot_Functions.validate_bot(self.bot, bot_info)
            if client_bot == None:
                return
            
            # Add to valid bots to clients dictionary
            self.clients[client_bot] = websocket
            print(f"Client {client_bot.name} connected.")

            # Handle incoming response from the client
            async for response in websocket:
                #Server <- Client
                client_response = json.loads(response)
                await Server_Bot_Functions.process_response(client_response)

        finally:
            # Remove the client from the dictionary if it disconnects
            if client_bot in self.clients:
                del self.clients[client_bot]
            print(f"Client {client_bot.name} disconnected.")

    #Server -> Clients
    async def broadcast_to_clients(self, message):
        # Send a message to all connected clients (game bots)
        if self.clients:
            server_message = json.dumps(message)
            await asyncio.wait([client.send(server_message) for client in self.clients.values()])

    #Server -> Client
    async def send_message_to_client(self, client_bot, message):
        if client_bot in self.clients:
            websocket = self.clients[client_bot]
            server_message = json.dumps(message)
            await websocket.send(server_message)
        else:
            print(f"Client {client_bot} not found.")
