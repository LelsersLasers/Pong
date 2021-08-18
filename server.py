"""
Description: Is the server portion of Pong, runs the game and sends data to client
Date: 8/17/21
Authors: Jerry and Millan
"""

import pygame
import random
import time
from Player import Player
from Vector import Vector
from Ball import Ball
import socket
from _thread import *
import pickle

# intial send should be ball, player1, player2, score

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

print("waiting for a connection.\n\nServer Started\n")
s.listen(2)

v1 = Vector(350, 250)
v2 = Vector(random.uniform(-1, 0.75), random.uniform(-1, 0.75))
ball = Ball(v1, v2)
player1 = Player(50, 250, 10, 50, 1, 0)
player2 = Player(650, 250, 10, 50, 2, 0)
score = [0, 0]
player = 1

gameData = [ball, player1, player2, score]

def threaded_client(conn, player):
    time.sleep(10)
    conn.send(pickle.dumps(player))
    conn.send(pickle.dumps(gameData))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            gameData[player] = data

            if not data:
                print("\nPlayer %i has disconnected.\n" % player)
                break
            else:
                print("Received from player %i" % player)
                print("    %s" % data)
                print("Sending to player %i" % player)
                print("    %s" % ball)

            conn.sendall(pickle.dumps(gameData))
        except:
            break

    print("Connection Lost\n\nQuitting game")
    conn.close()

def main():
    global player
    clock = pygame.time.Clock()
    while player <= 2:
        conn, addr = s.accept()
        print("Player", player, "connected to", addr)
        start_new_thread(threaded_client, (conn, player))
        player += 1


    print("Everyone connected.\n\nGame starting in 10 seconds\n")
    time.sleep(10)
    run = True
    while run:
        if gameData[3][0] >= 11:
            run = False
            print("Player 1 wins!")
            winner = "Player 1"
        elif gameData[3][0] >= 11:
            run = False
            print("Player 2 wins!")
            winner = "Player 2"

        gameData[0].checkHit(gameData[3], gameData[1], gameData[2])
        gameData[0].move() # Moves Ball
        clock.tick(60)

    print("%s won!" % winner)
    conn.close()

main()
