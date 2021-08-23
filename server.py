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
ball = Ball(v1)
player1 = Player(50, 250, 10, 50, 1, 0)
player2 = Player(650, 250, 10, 50, 2, 0)
score = [0, 0]
player = 1

gameData = [ball, player1, player2, score]
gameSelected = False

def setup(previousGamemode): # Is in server

    if previousGamemode == -1:
        choices = ["Choose gamemode", "Quit"]
        for i in range(1, len(choices) + 1):
            print("%i) %s" % (i, choices[i-1]))
    else:
        choices = ["Play again", "Change gamemode", "Quit"]
        for i in range(1, len(choices) + 1):
            print("%i) %s" % (i, choices[i-1]))

    badInput = True
    while badInput:
        choice = input("Please choose from above: ")
        try:
            index = int(choice)
            if previousGamemode != -1:
                index = index - 1
            badInput = False
        except:
            print("\nPlease choose from options above \n")

    print()
    gamemode = -1
    if index == 1:
        choices = ["Regular Pong", "Fog of War Pong", "4 Person Pong"]
        for i in range(1, len(choices) + 1):
            print("%i) %s" % (i, choices[i-1]))
        badInput = True
        while badInput:
            choice = input("Please choose from above: ")
            try:
                gamemode = int(choice)
                gamemode = gamemode - 1
                badInput = False
            except:
                print("Please choose 1, 2, or 3")
    return index, gamemode

def threaded_client(conn, player):
    time.sleep(3)
    conn.send(pickle.dumps(player))
    while True:
        global gameSelected
        if gameSelected == True:
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
                    print("\nConnection Lost\n\nQuitting game")
                    conn.close()
                    return



def playRegPong():
    print("Playing Regular Pong")
    global gameSelected
    run = True
    gameSelected = True
    while run:
        if gameData[3][0] >= 11:
            run = False
            print("Player 1 wins!")
            winner = "Player 1"
        elif gameData[3][1] >= 11:
            run = False
            print("Player 2 wins!")
            winner = "Player 2"

        gameData[0].checkHit(gameData[3], gameData[1], gameData[2])
        gameData[0].move() # Moves Ball
        clock.tick(60)

    print("%s won!" % winner)
    gameSelected = False

def playFogOfWar():
    print("Playing fog of war pong")

def play4Person():
    print("Playing 4 person Pong")

def chooseGamemode():
    previousGamemode = -1
    keepPlaying = True
    global gameSelected
    while keepPlaying:
        choice, gamemode = setup(previousGamemode)
        if choice == 0:
            if previousGamemode == 0:
                gameSelected = True
                playRegPong()
            elif previousGamemode == 1:
                gameSelected = True
                playFogOfWar()
            else:
                gameSelected = True
                play4Person()
        elif choice == 1:
            if gamemode == 0:
                gameSelected = True
                playRegPong()
                previousGamemode = 0
            elif gamemode == 1:
                gameSelected = True
                playFogOfWar()
                previousGamemode = 1
            else:
                gameSelected = True
                play4Person()
                previousGamemode = 2
        else:
            print("Quitting game")
            break


clock = pygame.time.Clock()

def main():
    global player
    while player <= 2:
        conn, addr = s.accept()
        print("Player", player, "connected to", addr)
        start_new_thread(threaded_client, (conn, player))
        player += 1


    print("Everyone connected. /nPlease choose which gamemode you would like to play")

    chooseGamemode()
    conn.close()

main()
