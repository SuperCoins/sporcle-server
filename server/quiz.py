class Quiz:
    def __init__(self, room, info):
        self.room = room
        self.info = info
        self.status = "ready"
        self._scoreboard = {}
        self.answer_trie = {}

    def update_status(self, status):
        self.status = status
        self.room.send_info()

    def start(self):
        self.update_status("in-progress")

    def end(self):
        self.update_status("done")

    def pause(self):
        self.update_status("paused")

    def unpause(self):
        self.update_status("in-progress")

    @property
    def scoreboard(self):
        return self._scoreboard

    @scoreboard.getter
    def scoreboard(self):
        return {player.name: score for player, score in self._scoreboard.items()}

    def correct_answer(self, player, answer):
        player_score = self._scoreboard.setdefault(player, {"points": 0, "answers": []})
        player_score["points"] += 1
        player_score["answers"].append(answer)
        self.room.send_info()

    def new_answer(self, word):
        current = self.answer_trie
        for letter in word:
            current = current.setdefault(letter, {})
        if "_end_" not in current:
            current["_end_"] = "_end_"
            return True
        else:
            return False
