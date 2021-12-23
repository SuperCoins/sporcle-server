import json
import websockets


def read(message):
    event = json.loads(message)
    return event


async def send(websocket, message):
    await websocket.send(json.dumps(message))


def broadcast(sockets, message):
    websockets.broadcast(sockets, json.dumps(message))


async def error(websocket, message):
    event = {"type": "error", "data": message}
    await send(websocket, event)
