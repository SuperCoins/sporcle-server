import asyncio
import websockets
import os
import signal
import random
import string
import sys
import logging
import json
import spacy
from profanity_filter import ProfanityFilter

sys.path.insert(0, "server")
from player import Player
from room import Room


ROOMS = {}
PLAYERS = {}

nlp = spacy.load("en_core_web_sm")
profanity_filter = ProfanityFilter(nlps={"en": nlp})
nlp.add_pipe(profanity_filter.spacy_component, last=True)


class LoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        try:
            websocket = kwargs["extra"]["websocket"]
            player = PLAYERS[websocket]
        except KeyError:
            return f" {msg}", kwargs
        return f"{player.name} {msg}", kwargs


logging.basicConfig(
    format="%(name)s:%(message)s",
    level=logging.DEBUG,
)
logger = LoggerAdapter(logging.getLogger("websockets"), {})


async def handler(websocket):
    try:
        async for message in websocket:
            event = read(message)
            player = PLAYERS.setdefault(
                websocket, Player(websocket, event.get("player", None))
            )
            if event["type"] == "join room":
                await join(event["data"], player)
            elif event["type"] == "create room":
                await host(player)
            else:
                await player.error("Please create or join a room first")
    finally:
        return


async def host(player):
    player.isHost = True
    room_code = generate_room_code()
    if not room_code:
        await player.error("Failed to generate an appropriate room code... somehow")
        return
    room = Room(room_code, player)
    ROOMS[room_code] = room
    try:
        await room.created()
        await play_host(player, room)
    except Exception as e:
        await player.error("Something went wrong creating a room: " + e)


async def join(room_code, player):
    try:
        room = ROOMS[room_code]
    except KeyError:
        await player.error("Room not found.")
        return

    await room.add_player(player)
    await play(player, room)


async def play_host(player, room):
    try:
        async for message in player.websocket:
            event = read(message)
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
                room.quiz.start()
            elif etype == "quiz end":
                room.quiz.end()
            elif etype == "quiz pause":
                room.quiz.pause()
            elif etype == "quiz unpause":
                room.quiz.unpause()
    finally:
        logging.info(f"{player.name} has left room {room.code}")
        await room.close("Host left, closing room!")
        del ROOMS[room.code]


async def play(player, room):
    try:
        async for message in player.websocket:
            event = read(message)
            if event["type"] == "submit answer":
                await room.answer(event["data"], player)
            elif event["type"] == "update name":
                await player.update_name(event["data"])
    finally:
        logging.info(f"{player.name} has left room {room.code}")
        await room.remove_player(player)


def read(message):
    return json.loads(message)


def generate_room_code():
    for i in range(20):
        code = "".join(random.choice(string.ascii_uppercase) for i in range(4))
        doc = nlp(code)
        if not doc._.is_profane and not code in ROOMS:
            return code


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8080"))
    async with websockets.serve(handler, "", port, logger=logger):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
