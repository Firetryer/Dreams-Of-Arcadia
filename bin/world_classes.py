import pygame
from .asset_loader import Assets
from . import tools
assets = Assets()

class Sprite(pygame.sprite.Sprite):	
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.MasterImage = assets.load(image)
		self.rect = self.MasterImage.get_rect()


	def set_layer(self, layer):
		self._layer = layer
		#LAYER 01 = Background
		#LAYER 02 = NONE
		#LAYER 03 = INTERACTABLES
		
class Backdrops(Sprite):
	def __init__(self, image):
		Sprite.__init__(self, image)
		self.rect.x = 0
		self.rect.y = 0

	def update(self):
		pass


class Clickable(Sprite):
	def __init__(self, image, x = 0, y = 0, name = "Clicky"):
		Sprite.__init__(self, image)
		self.name = name
		self.rect.x = x
		self.rect.y = y



	def update(self):
		pass