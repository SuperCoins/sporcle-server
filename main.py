import asyncio
import websockets
import secrets
import messages
import os
import signal

from server import Server

SERVERS = {}


async def handler(websocket):
    message = await websocket.recv()
    event = messages.read(message)
    if event["type"] == "join room":
        await join(websocket, event["data"])
    elif event["type"] == "create room":
        await host(websocket)
    else:
        await messages.error(websocket, "Please create or join a room first")


async def host(host):
    join_key = secrets.token_urlsafe(12)
    server = Server(join_key, host)
    SERVERS[join_key] = server
    try:
        await server.room_created()
        await play_host(host, server)
    except Exception as e:
        print(e)
        await messages.error(host, "Something went wrong creating a server.")


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
            if event["type"] == "answer response":
                await server.answer_response(
                    event["data"]["response"],
                    event["data"]["answer"],
                    event["data"]["player"],
                )
    finally:
        print("Host left, shutting down server")
        del SERVERS[server.id]


async def play(player, server):
    try:
        async for message in player:
            event = messages.read(message)
            if event["type"] == "submit answer":
                await server.answer(event["data"], player)
    finally:
        await server.remove_player(player)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8080"))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
