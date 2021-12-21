import json
import websockets


def read(message):
    event = json.loads(message)
    print("[" + event["type"] + "] " + message)
    return event


async def send(websocket, message):
    await websocket.send(json.dumps(message))
    print("(sent) ", message)


async def broadcast(sockets, message):
    await websockets.broadcast(sockets, json.dumps(message))
    print("(broadcast) ", message)


async def error(websocket, message):
    event = {"type": "error", "data": message}
    await send(websocket, event)
