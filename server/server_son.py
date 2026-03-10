import socket
import threading
import random

clients = []

objs = []
y = 600
for i in range(100):
    x = random.randint(12,88)*5
    objs.append(x)
    y -= random.randint(120,180)
    objs.append(y)

text = "obj"
for i in range(200):
    text += "," + str(objs[i])

def handle_client(client_socket, addr):
    buffer = ""

    answer(text)

    while True:
        try:
            chunk = client_socket.recv(1024).decode()
            if not chunk:
                break

            buffer += chunk

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)

                data = msg.split(",")

                if data[0] == "move":
                    broadcast(msg, client_socket)

                elif data[0] == "win":
                    broadcast(msg, client_socket)

                else:
                    broadcast(msg, client_socket)

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)

    broadcast("lose", client_socket)
    client_socket.close()
    print(f"[-] {addr} disconnected")


def broadcast(msg, sender_socket):
    for client in clients[:]:
        if client != sender_socket:
            try:
                client.send((msg + "\n").encode())
            except:
                clients.remove(client)


def answer(msg):
    for client in clients[:]:
        try:
            client.send((msg + "\n").encode())
        except:
            clients.remove(client)


def server_son(port):

    host = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("server started")

    while True:
        client_socket, addr = server.accept()

        print(f"[+] {addr} connected.")

        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()