import pygame
import json

class Camera:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.follow = None
		self.offset_width = 100
		self.offset_height = 100
		with open("bin/settings.json") as settings:
			self.settings = json.load(settings)
		reso = self.settings['resolution']
		if reso['x'] < 1920 and reso['y'] < 1080:
			self.offset_width  = reso['x'] / 1920 * 100			
			self.offset_height = reso['y'] / 1080 * 100

	def set_focus(self, sprite):
		self.x = self.sprite.x
		self.y = self.sprite.y

	def display(self, screen, sprite_group):

		for sprites in sprite_group:
			screen.blit(sprites.image, ((sprites.rect.x * (self.offset_width / 100)) - self. x, (sprites.rect.y * (self.offset_height / 100)) - self.y))