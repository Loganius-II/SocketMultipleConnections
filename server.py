

import socket
import threading
HEADER = 64
PORT = 8080
SERVER = '192.168.1.140'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((SERVER, PORT))
clientsList = []
nameList = []
def handle_client(client, addr):
    name = client.recv(1024).decode()
    while True:
        checkIt = check_for_name_dupe(name)
        if checkIt == True:
            client.send("YOURGOODTOGO".encode())
            break
        elif checkIt == False:
            client.send("NOTGOODTOGO".encode())
    print(f"[NEW CONNECTION] {name} connected")
    connected = True
    clientsList.append(client)
    while connected:
        try:
            msg = client.recv(1024).decode()
            print(f"[{name}] {msg}")
            if msg == '!DISCNCT!':
                connected = False

            broadcast(msg, client,name)
        except:
            broadcast(f"[{name}] Disconnected from chat", "server", None)

            connected = False

            nameList.remove(name)

    client.close()


def check_for_name_dupe(name) -> bool:
    if name in nameList:
        return False
    else:
        nameList.append(name)
        return True
def broadcast(msg, clientThatSent,name):
    if clientThatSent == "server":
        for client in clientsList:
            try:
                client.send(msg.encode())

            except:
                clientsList.remove(client)
    else:
        for client in clientsList:
            try:
                if client != clientThatSent:
                    client.send(f"[{name}]: {msg}".encode())
                    print(msg)
                else:
                    pass
            except:
                clientsList.remove(client)
def admin_input() -> None:
    while True:
        command = input()
        if '/get ' in command:
            if ' -IP ' in command:
                commandBreakList = command.split()
                index = 1
                for word in commandBreakList:
                    if index == 3:
                        if word in nameList:
                            index1 = nameList.index(word)
                            print(f"[IP] {word}: {clientsList[index1]}")
                        else:
                            print("[ERROR] Name not found")
                    else:
                        index += 1
        elif'/broadcast' in command:
            if '/broadcast -a -m' in command:
                commandBreakList = command.split()
                msg = ''
                for indexOf, value in enumerate(commandBreakList):
                    if indexOf >= 3:
                        msg += f"{value} "

                    else:
                        pass
                broadcast(f"[ADMIN] {msg}", "server", None)
            elif '/broadcast -p ' in command:
                commandBreakList = command.split()
                for indexOf, value in enumerate(commandBreakList):
                    if indexOf == 2:
                        if value in nameList:
                            indexOfName = nameList.index(value)
                            client = clientsList[indexOfName]
                            msg = ''
                            for indexOf, value in enumerate(commandBreakList):
                                if indexOf >= 4: 
                                    msg += f"{value} "

                                else:
                                    pass
                            client.send(f"[ADMIN] (Private): {msg}".encode())
                        else:
                            print(f"[ERROR] Name: {value} not found")
                    else:
                        pass

def start():
    server.listen()
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client,addr))
        thread2 = threading.Thread(target=admin_input, args=())
    
        thread.start()
        thread2.start()
        update = f"[ACTIVE CONNECTIONS] {threading.active_count() -2} "
        print(update)
        broadcast(update, "server", None)
print("[STARTING] Server starting")
start()
