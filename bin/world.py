import pygame
from world_classes import *


class ArcadeEntrance(Screen):
	def __init__(self):
		Screen.__init__(self)
		self.create_rooms()

	def create_rooms(self):
		self.background = Backdrops('Arcade01')
		self.chr = Clickable('Thomas01', 500, 600, 'Thomas')
		self.sg_all.add(self.background)
		self.sg_all.add(self.chr)
		self.sg_clickables.add(self.chr)


class Screen:
	def __init__(self):
		self.sg_all        = pygame.sprite.Group()
		self.sg_clickables = pygame.sprite.Group()

	def update(self):
		

	def render(self):
		pass

	def handle_events(self):
		pass


class World:
	def __init__(self):
		pass

	def update(self):
		pass

	def render(self):
		pass

	def handle_events(self):
		pass