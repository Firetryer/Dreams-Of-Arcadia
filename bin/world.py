import pygame
from .world_classes import *
from . camera import Camera
from . import tools
from . import world_rooms
import json




class World:
	def __init__(self):
		self.camera = Camera()
		self.current_screen = world_rooms.ArcadeEntrance(self, self.camera)

	def set_screen(self, newscreen):
		pass

	def update(self):
		self.current_screen.update()

	def render(self, screen):
		self.current_screen.render(self.camera, screen)
		

	def handle_events(self, event):
		self.current_screen.handle_events(event)


class Screen_Manager:
	def __init__(self):
		with open('bin/configs/world_locations.json') as location:
			self.scene_configs = json.load(locations)
		
		self.scenes = []

	def create_rooms(self):


class Dialog_Manager():
	def __init__(self):
		pass