import asyncio
import websockets
import secrets
import messages

from server import Server

SERVERS = {}


async def handler(websocket):
    message = await websocket.recv()
    event = messages.read(message)
    assert event["type"] == "init"
    if "data" in event:
        await join(websocket, event["data"])
    else:
        await host(websocket)


async def host(host):
    join_key = secrets.token_urlsafe(12)
    server = Server(join_key, host)
    SERVERS[join_key] = server
    try:
        event = {"type": "init", "data": join_key}
        await messages.send(host, event)
        await play_host(host, server)
    except:
        messages.error(host, "Something went wrong creating a server.")

async def join(player, join_key):
    try:
        server = SERVERS[join_key]
    except KeyError:
        await messages.error(player, "Server not found.")
        return

    await server.add_player(player, secrets.token_urlsafe(12))
    await play(player, server)

async def play_host(host, server):
    try:
        async for message in host:
            event = messages.read(message)
    finally:
        print('Host left, shutting down server')
        del SERVERS[server.id]


async def play(player, server):
    try:
        async for message in player:
            event = messages.read(message)
            if event["type"] == "answer":
                await server.answer(event["data"], player)
    finally:
        await server.remove_player(player)


async def main():
    async with websockets.serve(handler, "", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
