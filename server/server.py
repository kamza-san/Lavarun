import socket
import threading
from server_son import server_son

clients = []
servers = []


def handle_client(client_socket, addr):
    print(f"[+] {addr} connected. - main")

    buffer = ""

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)
                print(str(addr) + " | " + msg)

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()
    print(f"[-] {addr} disconnected - main")


def answer(msg, client):
    try:
        client.send((msg + "\n").encode())
    except:
        if client in clients:
            clients.remove(client)


def main_server():
    host = "0.0.0.0"
    port = 20000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[+] Server listening on {host}:{port}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    print("your ipv4 : %s" %(str(ip)))

    user_port = 20001

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

        if len(clients) >= 2:
            c1 = clients.pop(0)
            c2 = clients.pop(0)

            answer("port," + str(user_port), c1)
            answer("port," + str(user_port), c2)

            t = threading.Thread(target=server_son, args=(user_port,))
            t.start()
            servers.append(t)

            user_port += 1


if __name__ == "__main__":
    main_server()