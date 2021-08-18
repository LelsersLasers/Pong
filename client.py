"""
Description: This is the client portion of the game, just displays the game, gets
             input from the user, and sends/receives from the server.
"""

import pygame
import tkinter
from Player import Player
from Ball import Ball
from network import Network

pygame.init()
size = (700, 500)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Pong Client v0.02")


def displayScore(score, win):
	fontForText = pygame.font.Font('freesansbold.ttf', 32)
	text = fontForText.render("%i - %i" % (score[0], score[1]), True, (255, 255, 255), (0, 0, 0))

	win.blit(text, (317, 30))

def displayWinnerScreen(winner, win):
	fontForText = pygame.font.Font('freesansbold.ttf', 32)
	text = fontForText.render("%s won" % (winner), True, (255, 255, 255), (0, 0, 0))
	fontForText = pygame.font.Font('freesansbold.ttf', 20)
	text2 = fontForText.render("Returning to menu")

	win.blit(text, (317, win.y / 2))
	win.blit(text2, (317, 400))

def redrawWindow(win, gameData):
    win.fill((0,0,0))
    pygame.draw.line(win, (255,255,255), [349, 0], [349, 500], 5)
    displayScore(gameData[3], win)
    gameData[1].draw(win)
    gameData[2].draw(win)
    gameData[0].draw(win)
    pygame.display.flip()


def main():
    maxScore = 11
    serverIP = input("Enter Server IP Address: ")
    n = Network(serverIP)
    if n.data == -1:
        main()

    clientNum = n.getData() # Game Data should be a list of ball, player1, player2, score
    print("Client number: ", clientNum)
    clock = pygame.time.Clock()
    gameData = n.getGameData()
    run = True

    while run:
        clock.tick(60)
        gameData = n.send(gameData[clientNum])

        if gameData[3][0] >= 11:
            run = False
            print("Player 1 wins!")
            winner = "Player 1"
        elif gameData[3][0] >= 11:
            run = False
            print("Player 2 wins!")
            winner = "Player 2"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        gameData[clientNum].move()
        redrawWindow(win, gameData)

    displayWinnerScreen(winner, win)


main()
