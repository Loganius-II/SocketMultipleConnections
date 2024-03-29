import socket
import threading
HEADER = 64
PORT = int(input("What port do you want: "))
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((SERVER, PORT))

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode()
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(HEADER).decode()
            if msg == "disconnect":
                connected = False
            print(f"[{addr}] {msg}")

    client.close()

def start():
    server.listen()
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1} ")
print("[STARTING] Server starting")
start()