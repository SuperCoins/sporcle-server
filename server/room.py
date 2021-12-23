import websockets
import json
from quiz import Quiz


class Room:
    def __init__(self, code, host):
        self.code = code
        self.host = host
        self.connected = set()
        self.connected.add(host)
        self.quiz = Quiz(self, {})
        # When a quiz is loaded a unique id can be sent so a history of quizes is searched
        self.quiz_history = []

    async def created(self):
        await self.host.send({"type": "room created", "data": self.code})
        self.send_info()

    async def add_player(self, player):
        if player.name in [player.name for player in self.connected]:
            await player.error("Name is already in use.")
            return
        self.connected.add(player)
        player.room = self
        await player.send(
            {"type": "room joined", "data": self.code, "player": player.name}
        )
        self.send_info()

    async def remove_player(self, player):
        player.room = None
        self.connected.remove(player)
        self.send_info()

    def add_quiz(self, quiz_info):
        self.quiz = Quiz(self, quiz_info)
        self.quiz_history.append(self.quiz)
        self.send_info()

    def send_info(self):
        event = {
            "type": "room info",
            "data": {
                "room": {"code": self.code},
                "players": list([player.name for player in self.connected if player != self.host]),
                "quiz": {
                    "info": self.quiz.info,
                    "status": self.quiz.status,
                    "scoreboard": self.quiz.scoreboard,
                },
            },
        }
        self.broadcast(event)

    async def answer(self, answer, player):
        if not self.quiz.new_answer(answer):
            return
        await self.host.send(
            {"type": "submit answer", "data": answer, "player": player.name}
        )

    async def answer_response(self, response, answer, player_name):
        for player in self.connected:
            if player.name != player_name:
                continue
            await player.send(
                {
                    "type": "answer response",
                    "data": {"answer": answer, "response": response},
                },
            )
            if response == "correct" and self.quiz:
                self.quiz.correct_answer(player, answer)

    def broadcast(self, message):
        websockets.broadcast(
            [player.websocket for player in self.connected], json.dumps(message)
        )

    async def close(self, message):
        self.broadcast({"type": "room closing", "data": message})
        for player in self.connected:
            await player.close()
