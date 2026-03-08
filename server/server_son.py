import socket
import threading
import random
import time

clients = []
start = 0

def handle_client(client_socket, addr):
    global start
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            data = list(msg.split(','))
            if data[0] == "len":
                answer("len"+","+str(len(clients)), client_socket)
            elif data[0] == "move":
                broadcast(f"{msg}", client_socket)
            elif data[0] == "play":
                start += 1
            elif data[0] == "cancel":
                start -= 1
            elif data[0] == "win":
                broadcast(f"{msg}", client_socket)
            else:
                broadcast(f"{msg}", client_socket)                

        except:
            break
        if start == 2:
            objs = []
            y = 600
            for i in range(100):
                x = random.randint(12,88)*5
                objs.append(x)
                y -= random.randint(120,180)
                objs.append(y)
            text = "obj"
            for i in range(200):
                text += ","+str(objs[i])
            answer(text)
            time.sleep(0.1)
            answer("start")
            start = 0
            
    clients.remove(client_socket)
    client_socket.close()

def broadcast(msg, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(msg.encode())
            except:
                pass


def answer(msg):
    for client in clients[:]:
        try:
            client.send(msg.encode())
        except Exception as e:
            print(f"[ERROR] send failed to {client.getpeername()}: {e}")
            clients.remove(client)

def server_son(port):
    host = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)


    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()