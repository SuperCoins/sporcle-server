import messages


class Server:
    code = ""
    players = []
    # I probably don't need this dict and array both
    player_dict = {}
    name_dict = {}

    def __init__(self, code, host):
        self.code = code
        self.host = host

    async def room_created(self):
        await messages.send(self.host, {"type": "room created", "data": self.code})
        await self.send_room_info()

    async def add_player(self, player, player_name):
        self.players.append(player)
        self.player_dict[player] = player_name
        self.name_dict[player_name] = player
        await messages.send(player, {"type": "room joined", "data": self.code})
        await messages.send(self.host, {"type": "player_joined", "data": player_name})
        await self.send_room_info()

    async def remove_player(self, player):
        player_name = self.player_dict[player]
        self.players.remove(player)
        del self.player_dict[player]
        del self.name_dict[player_name]
        await messages.send(self.host, {"type": "player_left", "data": player_name})
        await self.send_room_info()

    async def send_room_info(self):
        event = {
            "type": "room info",
            "data": {
                "room": {"code": self.code},
                "players": list(self.name_dict.keys()),
            },
        }
        await messages.send(self.host, event)

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
