import asyncio
import websockets
import secrets
import messages
import os
import signal
import random
import string

from server import Server

SERVERS = {}


async def handler(websocket):
    message = await websocket.recv()
    event = messages.read(message)
    if event["type"] == "join room":
        await join(websocket, event["data"], event.get('player', None))
    elif event["type"] == "create room":
        await host(websocket)
    else:
        await messages.error(websocket, "Please create or join a room first")


async def host(host):
    room_code = "".join(random.choice(string.ascii_uppercase) for i in range(4))
    server = Server(room_code, host)
    SERVERS[room_code] = server
    try:
        await server.room_created()
        await play_host(host, server)
    except Exception as e:
        print(e)
        await messages.error(host, "Something went wrong.")


async def join(player, room_code, name):
    try:
        server = SERVERS[room_code]
    except KeyError:
        await messages.error(player, "Server not found.")
        return

    if not name:
        name = "".join(random.choice(string.ascii_uppercase) for i in range(4))
    await server.add_player(player, name)
    await play(player, server)


async def play_host(host, server):
    try:
        async for message in host:
            event = messages.read(message)
            etype = event["type"]
            print("event", event)
            if etype == "answer response":
                await server.answer_response(
                    event["data"]["response"],
                    event["data"]["answer"],
                    event["data"]["player"],
                )
            elif etype == "quiz info":
                server.add_quiz(event["data"])
            elif etype == "quiz start":
                print("quiz", server.quiz)
                server.quiz.start()
            elif etype == "quiz end":
                server.quiz.end()
            elif etype == "quiz pause":
                server.quiz.pause()
            elif etype == "quiz unpause":
                server.quiz.unpause()
    finally:
        print("Host left, shutting down server")
        del SERVERS[server.code]


async def play(player, server):
    try:
        async for message in player:
            event = messages.read(message)
            if event["type"] == "submit answer":
                await server.answer(event["data"], player)
            elif event["type"] == "update name":
                await server.update_player(player, event["data"])
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
