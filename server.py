import websockets
import json
import messages

class Server:
    id = ''
    players = []

    def __init__(self, id, host):
        self.id = id
        self.host = host

    def add_player(self, player):
      self.players.append(player)
      print("player was added to the game")
    
    def remove_player(self, player):
      self.players.remove(player)
      messages.broadcast(self.players, {"type": "player_left", "data": "player has left the game"})
