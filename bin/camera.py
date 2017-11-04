import pygame
import json
from . import tools
class Camera:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.follow = None

	def set_focus(self, sprite):
		self.x = self.sprite.x
		self.y = self.sprite.y

	def display(self, screen, sprite_group):

		for sprites in sprite_group:
			x, y = sprites.rect.x, sprites.rect.y
			if sprites._inworld:
				x, y = tools.world_to_screen(x, y)
			screen.blit(sprites.image, (x - self.x, y - self.y))

