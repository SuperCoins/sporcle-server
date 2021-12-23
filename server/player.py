import random
import string
import json


class Player:
    def __init__(self, websocket, name):
        self.websocket = websocket
        if name:
            self.name = name
        else:
            self.name = "".join(random.choice(string.ascii_uppercase) for i in range(4))
        self._isHost = False
        self.room = None

    @property
    def isHost(self):
        return self._isHost

    @isHost.setter
    def isHost(self, value):
        self._isHost = value
        if self._isHost:
            self.name = "HOST"

    async def update_name(self, value):
        self.name = value
        await self.send({"type": "name updated", "data": self.name})
        if self.room:
            self.room.send_info()

    async def send(self, message):
        if self.websocket.open:
            await self.websocket.send(json.dumps(message))

    async def error(self, message):
        event = {"type": "error", "data": message}
        await self.send(event)

    async def close(self):
        if self.websocket.open:
            await self.websocket.close()
