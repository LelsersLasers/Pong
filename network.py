"""
Description: This file allows the server and client to connect with each other and
             send/receive data on the game.
"""

import socket
import pickle # Sends objects over a network


class Network():
    def __init__(self, serverIP):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.data = self.connect() # Data should be a list of ball, player 1, player 2

    def getData(self):
        return self.data

    def connect(self):
        for i in range(4):
            try:
                self.client.connect(self.addr)
                return pickle.loads(self.client.recv(2048 * 2))
            except:
                print("\nConnection failed, please try again.\n")
                if i == 3:
                    return -1

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e, "\nThere was a problem with connection.\n\nReconnecting...")

    def getGameData(self):
        try:
            return pickle.loads(self.client.recv(2048 * 2))
        except:
            print("\nConnection failed")
