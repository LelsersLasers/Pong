import math

class Vector():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def addAndReturn(self, otherVector, speed):
		a = math.sqrt(otherVector.x**2 + otherVector.y**2)
		newX = self.x + (otherVector.x/a) * speed
		newY = self.y + (otherVector.y/a) * speed
		newVector = Vector(newX, newY)
		return newVector

	def get(self):
		return (self.x, self.y)