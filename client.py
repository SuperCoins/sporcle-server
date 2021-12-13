import socket
import errno
import sys


def decode(message: str):
    return message.decode("utf-8")


def encode(message: str):
    return message.encode("utf-8")


class Client:
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 1234

    def __init__(self):
        self.username = input("Username: ")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))
        self.socket.setblocking(False)  # Receive won't be blocking
        self.send_message(self.username)

    def send_message(self, message):
        message = encode(message)
        message_header = encode(f"{len(message):<{self.HEADER_LENGTH}}")
        self.socket.send(message_header + message)

    def receive_message(self):
        message_header = self.socket.recv(self.HEADER_LENGTH)
        if not len(message_header):
            print("connection closed by the server")
            sys.exit()
        message_length = int(decode(message_header))
        message = decode(self.socket.recv(message_length))
        return message

    def listen(self):
        while True:
            message = input(f"{self.username} > ")
            if message:
                self.send_message(message)
            try:
                while True:
                    username = self.receive_message()
                    message = self.receive_message()
                    print(f"{username} > {message}")
            except IOError as e:
                # there are no more messages to be received
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error", str(e))
                    sys.exit()
                continue  # these errors are fine, continue

            except Exception as e:
                print("General error", str(e))
                sys.exit()


client = Client()
client.listen()
