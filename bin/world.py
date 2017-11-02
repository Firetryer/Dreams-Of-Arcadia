import pygame
from .world_classes import *
from .camera import Camera



class Screen:
	def __init__(self, World):
		self.sg_all        = pygame.sprite.LayeredUpdates()
		self.sg_clickables = pygame.sprite.LayeredUpdates()

	def update(self):
		self.sg_all.update()

	def render(self):
		pass

	def handle_events(self):
		pass



class ArcadeEntrance(Screen):
	def __init__(self, world):
		Screen.__init__(self, world)
		self.create_rooms()

	def create_rooms(self):
		self.background = Backdrops('Arcade01')
		self.background.set_layer(1)
		self.chr = Clickable('Thomas01', 400, 440, 'Thomas')
		self.chr.image= pygame.transform.scale(self.chr.image, (int(self.chr.rect.width*0.7), int(self.chr.rect.height*0.7)))
		self.chr.set_layer(2)
		self.sg_all.add(self.background)
		self.sg_all.add(self.chr)
		self.sg_clickables.add(self.chr)





class World:
	def __init__(self):
		self.camera = Camera()
		self.current_screen = ArcadeEntrance(self)

	def set_screen(self, newscreen):
		pass

	def update(self):
		pass

	def render(self, screen):
		self.camera.display(screen, self.current_screen.sg_all)

	def handle_events(self):
		pass