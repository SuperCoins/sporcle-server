class Quiz:
    info = {}
    server = ""
    status = "ready"

    def __init__(self, server, info):
        self.server = server
        self.info = info

    def update_status(self, status):
        print('self', self)
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
