import socket 
import threading 

HEADER = 64
PORT = 8080
SERVER = '192.168.1.140'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
access = False
while not access:
    name = input("Name: ")
    client.send(name.encode())
    check = client.recv(1024).decode()
    if check == "YOURGOODTOGO":
        access = True
        break
    else:

        print("Name already in use")
try:
    def send(msg):
        message = msg.encode()
        client.send(message)

    def recieve():
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                print("[SERVER] Shutdown")
            print(msg)
    connected = True
    thread = threading.Thread(target=recieve, args=())
    thread.start()
    while connected:
        mess = input("")
        send(mess)
        if mess == '!DISCNCT!':
            connected = False
except:
    print("[DISCONNECTED] Server shut down")