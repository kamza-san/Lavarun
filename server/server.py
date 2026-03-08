import socket
import threading
from server_son import server_son
import time

clients = []
severs = []

def handle_client(client_socket, addr):
    global start
    print(f"[+] {addr} connected.")
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(client_socket+" | "+msg)
        except:
            break

def all_answer(msg):
    print("server | "+msg)
    for client in clients[:]:
        try:
            client.send(msg.encode())
        except Exception as e:
            print(f"[ERROR] send failed to {client.getpeername()}: {e}")
            clients.remove(client)

def answer(msg,client):
    print(client+" | "+msg)
    try:
        client.send(msg.encode())
    except Exception as e:
        print(f"[ERROR] send failed to {client.getpeername()}: {e}")
        clients.remove(client)

def main_server():
    host = '0.0.0.0'
    port = 20000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[+] Server listening on {host}:{port}")

    user_port = 20001
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        if len(clients) >= 2:
            answer(user_port,clients[0])
            answer(user_port,clients[1])
            severs.append(threading.Thread(target=server_son, args=(user_port)))
            user_port += 1

if __name__ == "__main__":
    main_server()