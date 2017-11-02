import pygame
from .asset_loader import *

class Sprite(pygame.sprite.Sprite):	
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		#Could have master image stored somewhere else.
		self.MasterImage = Assets.load(image)
		self.image = self.MasterImage.copy()
		self.rect = self.image.get_rect()
		self.imageCenter = self.rect.width / 2, self.rect.height / 2


class Backdrops(Sprite):
	def __init__(self, image):
		Sprite.__init__(self, image)
		self.rect.x = 0
		self.rect.y = 0


class Clickable(Sprite):
	def __init__(self, image, x = 0, y = 0, name = "Clicky"):
		Sprite.__init__(self, image)

		self.name = name
		self.rect.x = x
		self.rect.y = y

	def update():
		pass