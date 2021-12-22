import asyncio
import websockets
import os
import signal
import random
import string
import sys

sys.path.insert(0, 'server')
import messages
from room import Room

ROOMS = {}


async def handler(websocket):
    message = await websocket.recv()
    event = messages.read(message)
    if event["type"] == "join room":
        await join(websocket, event["data"], event.get("player", None))
    elif event["type"] == "create room":
        await host(websocket)
    else:
        await messages.error(websocket, "Please create or join a room first")


async def host(host):
    # TODO Make sure the room doesn't already exist
    room_code = "".join(random.choice(string.ascii_uppercase) for i in range(4))
    room = Room(room_code, host)
    ROOMS[room_code] = room
    try:
        await room.created()
        await play_host(host, room)
    except Exception as e:
        await messages.error(host, "Something went wrong: " + e)


async def join(player, room_code, name):
    try:
        room = ROOMS[room_code]
    except KeyError:
        await messages.error(player, "Room not found.")
        return

    if not name:
        name = "".join(random.choice(string.ascii_uppercase) for i in range(4))
    await room.add_player(player, name)
    await play(player, room)


async def play_host(host, room):
    try:
        async for message in host:
            event = messages.read(message)
            etype = event["type"]
            if etype == "answer response":
                await room.answer_response(
                    event["data"]["response"],
                    event["data"]["answer"],
                    event["data"]["player"],
                )
            elif etype == "quiz info":
                room.add_quiz(event["data"])
            elif etype == "quiz start":
                print("quiz", room.quiz)
                room.quiz.start()
            elif etype == "quiz end":
                room.quiz.end()
            elif etype == "quiz pause":
                room.quiz.pause()
            elif etype == "quiz unpause":
                room.quiz.unpause()
    finally:
        room.close("Host left, closing room!")
        del ROOMS[room.code]


async def play(player, room):
    try:
        async for message in player:
            event = messages.read(message)
            if event["type"] == "submit answer":
                await room.answer(event["data"], player)
            elif event["type"] == "update name":
                await room.update_player(player, event["data"])
    finally:
        await room.remove_player(player)


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
