import asyncio
import websockets
import json


class Websocket:
    def __init__(self):
        # WebScoket server URI (local or remote)
        self.HOST = 'localhost'
        self.PORT = 3000
        self.WEBSOCKET_URI = 'ws://localhost:3000' # Change this to your WebSocket URI