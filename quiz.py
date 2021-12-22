class Quiz:
    info = {}
    server = ""
    status = "ready"
    scoreboard = {}
    answers = {}

    def __init__(self, server, info):
        self.server = server
        self.info = info

    def update_status(self, status):
        self.status = status
        self.server.send_room_info()

    def start(self):
        self.update_status("in-progress")

    def end(self):
        self.update_status("done")

    def pause(self):
        self.update_status("paused")

    def unpause(self):
        self.update_status("in-progress")

    def correct_answer(self, player_name, answer):
        if player_name not in self.scoreboard:
            self.scoreboard[player_name] = {"points": 0, "answers": []}
        self.scoreboard[player_name]["points"] += 1
        self.scoreboard[player_name]["answers"].append(answer)
        self.server.send_room_info()
