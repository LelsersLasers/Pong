import pygame
import random
from Vector import Vector


class Ball():
	def __init__(self, vector):
		self.speed = 3
		self.vector = vector
		self.color = (255, 255, 255)
		self.size = 7
		self.rect = (self.vector.x, self.vector.y, self.size, self.size)

		self.resetDir()

		if self.vector.x > -0.3 and self.vector.x < 0.3:
			if self.vector.x < 0:
				self.vector.x = -0.3
			else:
				self.vector.x = 0.3

	def __str__(self):
		return "Ball: X: %i; Y: %i" % (self.vector.x, self.vector.y)

	def resetDir(self):
		self.direction = Vector(random.uniform(-1, 1), random.uniform(-1, 1))

	def draw(self, win):
		pygame.draw.circle(win, self.color, self.vector.get(), self.size, self.size)

	def move(self):
		self.vector = self.vector.addAndReturn(self.direction, self.speed)
		self.rect = (self.vector.x, self.vector.y, self.size, self.size)

	def checkHit(self, score, player1, player2):

		if self.vector.x <= 0 + self.size:
			self.direction.x = 0 - self.direction.x
			score[1] += 1
			self.vector.x = 350
			self.vector.y = 250
			self.speed = self.speed * 1.01
			self.resetDir()
		elif self.vector.x >= 700 - self.size:
			self.direction.x = 0 - self.direction.x
			self.vector.x = 350
			self.vector.y = 250
			score[0] += 1
			self.speed = self.speed * 1.01
			self.resetDir()
		elif self.vector.y <= 0 + self.size:
			self.direction.y = 0 - self.direction.y
			self.speed = self.speed * 1.01
		elif self.vector.y >= 500 - self.size:
			self.direction.y = 0 - self.direction.y
			self.vector.y = 500 - self.size - 1
			self.speed = self.speed * 1.01
		elif self.vector.y >= player1.y and self.vector.y <= player1.y + player1.height and self.vector.x >= player1.x and self.vector.x <= player1.x + player1.width:
			self.direction.x = 0 - self.direction.x
			self.speed = self.speed * 1.01
		elif self.vector.y >= player2.y and self.vector.y <= player2.y + player2.height and self.vector.x >= player2.x and self.vector.x <= player2.x + player2.width:
			self.direction.x = 0 - self.direction.x
			self.speed = self.speed * 1.01
