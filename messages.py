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
  event = json.loads(message)
  await websockets.broadcast(sockets, message)
  print("(broadcast) ", message)