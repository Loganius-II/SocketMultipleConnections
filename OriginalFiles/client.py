import socket 
import threading 

HEADER = 64
PORT = int(input("What port do you want: "))
SERVER = '192.168.1.140'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


def send(msg):
    message = msg.encode()
    msg_length = len(message)
    send_length = str(msg_length).encode()
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)