import messages


class Server:
    code = ""
    connected = set()
    # I probably don't need this dict and array both
    player_dict = {}
    name_dict = {}
    quiz_status = 'None'

    def __init__(self, code, host):
        self.code = code
        self.host = host
        self.connected.add(host)

    async def room_created(self):
        await messages.send(self.host, {"type": "room created", "data": self.code})
        self.send_room_info()

    async def add_player(self, player, player_name):
        self.connected.add(player)
        self.player_dict[player] = player_name
        self.name_dict[player_name] = player
        await messages.send(player, {"type": "room joined", "data": self.code})
        self.send_room_info()

    async def remove_player(self, player):
        player_name = self.player_dict[player]
        self.connected.remove(player)
        del self.player_dict[player]
        del self.name_dict[player_name]
        self.send_room_info()

    async def update_quiz_status(self, status):
        self.quiz_status = status
        self.send_room_info()

    def send_room_info(self):
        event = {
            "type": "room info",
            "data": {
                "room": {"code": self.code},
                "players": list(self.name_dict.keys()),
                "quiz": self.quiz_status
            },
        }
        messages.broadcast(self.connected, event)

    async def answer(self, answer, player):
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
