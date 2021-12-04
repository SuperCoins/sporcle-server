import socket
import time
import pickle

HEADERSIZE = 10

# ipv4 = AF_INET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This is the port we're binding it to, localhost for the moment
s.bind((socket.gethostname(), 1234))
# Queue of 5
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    d = {1: "hi", 2: "there"}
    msg = pickle.dumps(d)  # this is already bytes

    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg

    clientsocket.send(msg)
