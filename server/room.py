import messages
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
        # I probably don't need this dict and array both
        self.player_dict = {}
        self.name_dict = {}

    async def created(self):
        await messages.send(self.host, {"type": "room created", "data": self.code})
        self.send_info()

    async def add_player(self, player, player_name):
        if player_name in self.player_dict.keys():
            await messages.error(player, "Name is already in use.")
            return
        self.connected.add(player)
        self.player_dict[player] = player_name
        self.name_dict[player_name] = player
        await messages.send(
            player, {"type": "room joined", "data": self.code, "player": player_name}
        )
        self.send_info()

    async def remove_player(self, player):
        player_name = self.player_dict[player]
        self.connected.remove(player)
        del self.player_dict[player]
        del self.name_dict[player_name]
        self.send_info()

    async def update_player(self, player, name):
        if name in self.player_dict.keys():
            await messages.error(player, "Name is already in use.")
            return
        current_name = self.player_dict[player]
        del self.name_dict[current_name]
        self.name_dict[name] = player
        self.player_dict[player] = name
        await messages.send(player, {"type": "name updated", "data": name})
        self.send_info()

    def add_quiz(self, quiz_info):
        self.quiz = Quiz(self, quiz_info)
        self.quiz_history.append(self.quiz)
        print(self.quiz.answer_trie)
        self.send_info()

    def send_info(self):
        event = {
            "type": "room info",
            "data": {
                "room": {"code": self.code},
                "players": list(self.name_dict.keys()),
            },
        }
        if self.quiz:
            event["data"]["quiz"] = {
                "info": self.quiz.info,
                "status": self.quiz.status,
                "scoreboard": self.quiz.scoreboard,
            }
        messages.broadcast(self.connected, event)

    async def answer(self, answer, player):
        if not self.quiz.new_answer(answer):
            return
        player_name = self.player_dict[player]
        await messages.send(
            self.host, {"type": "submit answer", "data": answer, "player": player_name}
        )

    async def answer_response(self, response, answer, player_name):
        player = self.name_dict[player_name]
        await messages.send(
            player,
            {
                "type": "answer response",
                "data": {"answer": answer, "response": response},
            },
        )
        if response == "correct" and self.quiz:
            self.quiz.correct_answer(player_name, answer)

    def close(self, message):
        messages.broadcast(
            self.player_dict.keys(), {"type": "room closing", "data": message}
        )