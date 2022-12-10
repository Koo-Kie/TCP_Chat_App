import re
import socket, threading

ip = "127.0.0.1"
port = 4444

username = input("Username: ")


def connexion():
    global s
    print('Connecting...')
    s = socket.socket()
    while True:
        try:
            s.connect((ip,port))
            s.send(username.encode('UTF-8'))
            print('Connected!')
            break
        except socket.error:
            continue

def receiver():
    try:
        while True:
            print(s.recv(1024).decode('UTF-8'))
    except socket.error:
        connexion()

connexion()
t = threading.Thread(target= receiver)
t.start()

try:    
    while True:
        message = input('>> ')
        if len(message.strip()) == 0:
            continue
        else:
            s.send(message.encode('UTF-8'))
except socket.error:
    connexion()