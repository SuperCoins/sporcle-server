import asyncio
import websockets
import json
import secrets

from server_class import Server

SERVERS = {}


def readMessage(message):
    event = json.loads(message)
    print("[" + event["type"] + "] " + message)
    return event


async def sendMessage(message, websocket):
    await websocket.send(json.dumps(message))
    print("(sent) ", message)


async def handler(websocket):
    message = await websocket.recv()
    event = readMessage(message)
    assert event["type"] == "init"
    if "data" in event:
        await join(websocket, event["data"])
    else:
        await start(websocket)


async def sendError(player, message):
    event = {"type": "error", "message": message}
    await sendMessage(event, player)


async def start(player):
    join_key = secrets.token_urlsafe(12)
    server = Server(join_key)
    SERVERS[join_key] = server
    server.add_player(player)
    try:
        event = {"type": "init", "data": join_key}
        await sendMessage(event, player)
        await play(player, server)
    except:
        sendError(player, "Something went wrong creating a server.")
    finally:
        del SERVERS[join_key]


async def join(player, join_key):
    try:
        server = SERVERS[join_key]
    except KeyError:
        await sendError(player, "Server not found.")
        return

    server.add_player(player)
    play(player, server)


async def play(player, server):
    try:
        async for message in player:
            event = readMessage(message)
            await sendMessage("thanks for the message", player)
    finally:
        server.remove_player(player)


async def main():
    async with websockets.serve(handler, "", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
