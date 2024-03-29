import socket
import threading

HEADER = 64
PORT = 8080
SERVER = '192.168.1.140'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
clientsList = []
nameList = []
addressList = []
banned_clients_list = []
def handle_client(client, addr):

    try:
        while True:
            name = client.recv(1024).decode()
            checkIt = check_for_name_dupe(name)
            if checkIt == True:
                client.send("YOURGOODTOGO".encode())
                break
            elif checkIt == False:
                client.send("NOTGOODTOGO".encode())
    except ConnectionResetError:
        print(f"[{name}] Disconnected")
        broadcast(f"[{name}] Disconnected", "server", None)
        connected = False
        nameList.remove(name)

        client.close()
        return

    updateName = f"[NEW CONNECTION] {name} connected"
    print(updateName)
    broadcast(updateName, "server", None)
    connected = True
    clientsList.append(client)
    addressList.append(addr)
    while connected:
        try:
            msg = client.recv(1024).decode()
            print(f"[{name}] {msg}")
            if msg == '!DISCNCT!':
                connected = False
                nameList.remove(name)
            else:
                broadcast(msg, client, name)
        except ConnectionResetError:
            print(f"[{name}] Disconnected")
            broadcast(f"[{name}] Disconnected", "server", None)
            connected = False
            nameList.remove(name)
            addressList.remove(addr)

            client.close()
            break
        except Exception as e:
            print(f"Error occurred for client {name}: {e}")
            connected = False
            nameList.remove(name)
            client.close()
            break

def check_for_name_dupe(name) -> bool:
    if name in nameList:
        return False
    elif ' ' in name:
        return False
    elif '' in name:
        return False
    else:
        nameList.append(name)
        return True

def broadcast(msg, clientThatSent, name):
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
            elif command == '/get -clients_list':
                print(clientsList)
            elif command == '/get -name_list':
                print(nameList)
        elif '/broadcast' in command:
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
        elif '/kick' in command:
            commandBreakList = command.split()
            name = commandBreakList[1]
            for index, value in enumerate(nameList):
                if value == name:
                    client_targ = clientsList[index]
                    client_targ.close()
                else:
                    pass
        elif '/ban' in command:
            commandBreakList = command.split()
            name = commandBreakList[1]
            for index, value in enumerate(nameList):
                if value == name:

                    banned_client = addressList[index]
                    client_client = clientsList[index]
                    banned_clients_list.append(banned_client)
                    client_client.close()
                else:
                    pass

def start():
    server.listen()
    while True:
        client, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(client, addr))
        admin_thread = threading.Thread(target=admin_input, args=())
        admin_thread.start()
        thread.start()
        update = f"[ACTIVE CONNECTIONS] {len(clientsList) + 1} "
        print(update)
        broadcast(update, "server", None)

print("[STARTING] Server starting")
start()
