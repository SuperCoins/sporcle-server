import socket
import select
import constants


def decode(message: str):
    return message.decode("utf-8")


class Server:
    sockets_list = []
    clients = {}  # key is socket id, value is user info

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows the server to reconnect to the same address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((constants.IP, constants.PORT))
        self.socket.listen()
        self.sockets_list.append(self.socket)

    # each message has a header with the length of the message, followed by the message
    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(constants.HEADER_LENGTH)
            # if there is no header then the client has sent nothing and has closed the connection
            if not len(message_header):
                return False
            message_length = int(decode(message_header))  # still converts even with whitespace
            return {
                "header": message_header,
                "data": client_socket.recv(message_length),
            }
        except:
            return False

    def connect_user(self):
        client_socket, client_address = self.socket.accept()
        user = self.receive_message(client_socket)
        if user is False:
            return False
        self.sockets_list.append(client_socket)
        self.clients[client_socket] = user
        print(f'Accepted new connection from {client_address[0]}:{client_address[1]} username:{decode(user["data"])}')

    def disconnect_user(self, client_socket):
        client_name = decode(self.clients[client_socket]["data"])
        self.sockets_list.remove(client_socket)
        del self.clients[client_socket]
        print(f"Closed connection from {client_name}")

    def send_client_message(self, notified_socket, message):
        user = self.clients[notified_socket]
        print(f'Sending message from {decode(user["data"])}: {decode(message["data"])}')

        for client_socket in self.clients:
            if client_socket != notified_socket:
                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

    def listen(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:
                # someone just connected
                if notified_socket == self.socket:
                    self.connect_user()
                else:
                    message = self.receive_message(notified_socket)
                    if message is False:
                        self.disconnect_user(notified_socket)
                        continue
                    self.send_client_message(notified_socket, message)

            for notified_socket in exception_sockets:
                self.disconnect_user(notified_socket)


server = Server()
server.listen()
