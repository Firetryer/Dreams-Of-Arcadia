import pygame
from .world_classes import *
from . camera import Camera
from . import tools
from . import world_rooms

class Screen:
	def __init__(self, World, Camera):
		self.camera = Camera
		self.sg_all        = pygame.sprite.LayeredUpdates()
		self.sg_clickables = pygame.sprite.LayeredUpdates()

	def update(self):
		self.sg_all.update()

	def render(self,camera,screen):
		camera.display(screen, self.sg_all)

	def handle_events(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			print(x, y)
			pos = tools.screen_to_world(x,y)
			for sprites in self.sg_clickables:
				print(sprites.rect)
				if sprites.rect.collidepoint(pos):
					print("CLICKED!")



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