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
    else:
        print("Name already in use or contains a space. Please choose another name.")

try:
    def send(msg):
        message = msg.encode()
        client.send(message)

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                print(msg)
            except:
                print("[SERVER] Disconnected from server")
                print("You were either kicked or the server shutdown")
                break

    connected = True
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    while connected:
        mess = input("")
        send(mess)
        if mess == '!DISCNCT!':
            connected = False

    print("[DISCONNECTED] Server shut down")
    receive_thread.join()

except:
    print("[DISCONNECTED] Server shut down")
    receive_thread.join()
