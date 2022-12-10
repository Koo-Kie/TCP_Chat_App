import socket
from threading import Thread

try:
    connections = []
    addresses = []
    ip = '127.0.0.1'
    port = 4444
    clients = 0

    def accept_connections(s):
        global clients
        while True:
            connection, address = s.accept()
            username = connection.recv(1024).decode('UTF-8')
            clients += 1
            print(f'Got connexion from {username}({address[0]})\nConnected: {clients}')
            for user in connections:
                user.send(f'{username} joined the discussion. Connected: {clients}'.encode('UTF-8'))
            connections.append(connection)
            addresses.append(f'{address};{username}')
            Thread(target= message_handler, args= (connection, username)).start()

    def message_handler(connection, username):
        global clients
        try:
            while True:
                message = connection.recv(1024).decode('UTF-8')
                for user in connections:
                    user.send(f'[{username}] {message}'.encode('UTF-8'))
                print(f'[{username}] {message}')
        except socket.error:
            clients -= 1
            print(f'{username} left the discussion.\n Connected: {clients}')
            connection.send(f'{username} left the discussion. Connected: {clients}'.encode('UTF-8'))

    s = socket.socket()
    s.bind((ip, port))
    print('Waiting for connections...')
    s.listen()
    Thread(target = accept_connections, args = (s,)).start()
except:
    quit('\nTerminating...')


