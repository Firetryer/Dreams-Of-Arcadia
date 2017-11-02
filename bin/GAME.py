import pygame
import world

class GameManager:
	def __init__(self):
		self.gameplay_list = {"world": world.world}
		self.current = self.gameplay_list['world']

	def update(self):
		self.current.update()

	def render(self):
		self.current.render()

	def handle_events(self):
		self.current.handle_events()