"""
Description: Plays pong in pygame using pygame graphics, vectors (seperate class) to figure out movement of the ball, increasing/decreasing y values of players to have players move. Which allows the players 
"""
import pygame
import tkinter
import random
from Player import Player
from Vector import Vector
from Ball import Ball

def displayWinnerScreen(winner, win):
	fontForText = pygame.font.Font('freesansbold.ttf', 32)
	text = fontForText.render("%s won" % (winner), True, (255, 255, 255), (0, 0, 0))
	fontForText = pygame.font.Font('freesansbold.ttf', 20)
	text2 = fontForText.render("Press Space to play again\n \nPress Enter to return to menu")

	win.blit(text, (317, win.y / 2))
	win.blit(text2, (317, 400))

def displayScore(score, win):
	fontForText = pygame.font.Font('freesansbold.ttf', 32)
	text = fontForText.render("%i - %i" % (score[0], score[1]), True, (255, 255, 255), (0, 0, 0))

	win.blit(text, (317, 30))


def setup(): # Is in server
	choices = ["1 player", "2 player local", "2 player with server", "0 player"]
	for i in range(1, len(choices) + 1):
		print("%i) %s" % (i, choices[i-1]))

	badInput = True
	while badInput:
		choice = input("Gamemode (1,2,4): ")
		try:
			index = int(choice)
			index = index - 1
			badInput = False
		except:
			print("Please choose 1, 2, or 4")
	dif = 0.0
	if index == 0:
		badInput = True
		while badInput:
			choice = input("Difficulty (1,2,3): ")
			try:
				dif = int(choice)
				dif = dif - 1
				badInput = False
			except:
				print("Please choose 1, 2, or 3")
	dif = dif / 4
	return index, dif
	

def main():
	gamemode, dif = setup()
	gameOn = True
	v1 = Vector(350, 250)
	v2 = Vector(random.uniform(-1, 0.75), random.uniform(-1, 0.75))
	ball = Ball(v1, v2)

	player = Player(50, 250, 10, 50, 1, 0)
	player2 = Player(650, 250, 10, 50, 2, dif)
	
	score = [0, 0]


	pygame.init()
	size = (700, 500)
	win = pygame.display.set_mode(size)
	pygame.display.set_caption("Pong")
	clock = pygame.time.Clock()

	gameOn = True

	while (gameOn):
		if score[0] >= 11:
			gameOn = False
			print("Player 1 wins!")
			winner = "Player 1"
		elif score[1] >= 11:
			gameOn = False
			print("Player 2 wins!")
			winner = "Player 2"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOn = False

		if gamemode == 0:
			player.move()
			player2.computerTry(ball)
		elif gamemode == 3:
			player2.computerTry(ball)
			player.computerTry(ball)
		elif gamemode == 1:
			player.move()
			player2.move()

		ball.checkHit(score, player, player2)
		ball.move()

		win.fill((0,0,0))
		pygame.draw.line(win, (255,255,255), [349, 0], [349, 500], 5)
		# pygame.draw.line(win, (255,255,255), [200, 0], [200, 200], 5)
		# pygame.draw.line(win, (255,255,255), [0, 200], [200, 200], 5)

		displayScore(score, win)
		player.draw(win)
		player2.draw(win)
		ball.draw(win)
		pygame.display.flip()

		clock.tick(60)
	# Make winner screen and login/loading screen
	score = [0, 0]
	displayWinnerScreen(winner, win)


main()
pygame.quit()