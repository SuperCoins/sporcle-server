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
        player_score = self.scoreboard.setdefault(player_name, {"points": 0, "answers": []})
        player_score["points"] += 1
        player_score["answers"].append(answer)
        self.server.send_room_info()
