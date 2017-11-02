import pygame
from . import world

class GameManager:
	def __init__(self):
		self.gameplay_list = {"world": world.World}
		self.current = self.gameplay_list['world']()

	def update(self):
		self.current.update()

	def render(self, screen):
		self.current.render(screen)

	def handle_events(self):
		self.current.handle_events()