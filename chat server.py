import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allows the server to reconnect to the same address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}  # key is socket id, value is user info

# each message has a header with the length of the message, followed by the message
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        # if there is no header then the client has sent nothing and has closed the connection
        if not len(message_header):
            return False
        message_length = int(
            message_header.decode("utf-8")
        )  # still converts even with whitespace
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # someone just connected
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(
                f'Accepted new connection from {client_address[0]}:{client_address[1]} username:{user["data"].decode("utf-8")}'
            )

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f'Closed connection from {clients[notified_socket]["data"].decode("utf-8")}'
                )
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(
                f'Recived message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}'
            )

            # Now we want to send this to others
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user["header"]
                        + user["data"]
                        + message["header"]
                        + message["data"]
                    )

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
