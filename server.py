import websockets
import json
import messages


class Server:
    id = ""
    players = []
    # I probably don't need this dict and array both
    player_dict = {}

    def __init__(self, id, host):
        self.id = id
        self.host = host

    async def add_player(self, player, player_name):
        self.players.append(player)
        self.player_dict[player] = player_name
        await messages.send(self.host, {"type": "player_joined", "data": player_name})

    async def remove_player(self, player):
        player_name = self.player_dict[player]
        self.players.remove(player)
        del self.player_dict[player]
        await messages.send(self.host, {"type": "player_left", "data": player_name})

    async def answer(self, answer, player):
        player_name = self.player_dict[player]
        await messages.send(
            self.host, {"type": "answer", "data": answer, "player": player_name}
        )
