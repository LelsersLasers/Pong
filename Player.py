import pygame

class Player():
	def __init__(self, x, y, width, height, player, difficulty):
		self.x = x
		self.y = y
		self.speed = 2 + difficulty # 0 .25 .5 (Only 0 for users, 0 for computer is easy)
		self.width = width
		self.height = height
		self.color = (255, 255, 255)
		self.rect = (x, y, width, height)
		self.player = player

	def __str__(self):
		return "Player: X: %i; Y: %i" % (self.x, self.y)
	def draw(self, win):
		pygame.draw.rect(win, self.color, self.rect)

	def move(self):
		keyPressed = pygame.key.get_pressed()
		if self.player == 1:
			key1 = pygame.K_UP
			key2 = pygame.K_DOWN
		else:
			key1 = pygame.K_w
			key2 = pygame.K_s
		if self.y > 0 and self.y + self.height < 500:
			if keyPressed[key1]:
				self.y -= self.speed
			if keyPressed[key2]:
				self.y += self.speed
		else:
			if self.y < 0:
				self.y = 1
			else:
				self.y = 499 - self.height

		self.update()

	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

	def computerTry(self, ball): # To add harder difficulty, we can just add to the comp's speed
		if ball.vector.y < self.y + self.height / 2:
			self.y -= self.speed
		elif ball.vector.y > self.y - self.height / 2:
			self.y += self.speed

		self.update()
