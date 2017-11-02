import pygame
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
			screen.blit(sprites.image, (sprites.rect.x + self. x, sprites.rect.y + self.y))