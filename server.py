import socket, base64
from cryptography.fernet import Fernet
import threading as thrdlib

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 808))
server.listen()

clients = []
nicknames = []

def handle(client):
    while True:
        msg = client.recv(1024)
        if msg.decode("utf-8") == ":exit":
            index = clients.index(client)
            client.close()
            clients.remove(clients[index])
            nicknamer = nicknames[index]
            nicknames.remove(nicknamer)
            broadcast(f"{nicknamer} exited the chat")
            break
        else:
            broadcast(f"{nicknames[clients.index(client)]}> {msg.decode('utf-8')}")

def broadcast(message):
    for client in clients:
        client.send(Fernet(base64.urlsafe_b64encode(b"AnonymousKeyAnonymousKey12345678")).encrypt(message.encode("utf-8")))

def receive():
    while True:
        client, address = server.accept()
        clients.append(client)

        nickname = client.recv(1024)
        nicknames.append(nickname.decode("utf-8"))

        broadcast(f"{nickname.decode('utf-8')} entered in the chat.")

        handle_thrd = thrdlib.Thread(target=handle, args=(client,))
        handle_thrd.start()

receive()
