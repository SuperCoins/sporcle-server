class Server:
    server_id = ''
    players = []

    def __init__(self, id):
        self.server_id = id

    def add_player(self, player):
      self.players.append(player)
      print("player was added to the game")
    
    def remove_player(self, player):
      self.players.remove(player)
      print("player was removed from the game")