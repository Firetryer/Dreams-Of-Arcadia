import pygame
from .world_classes import *

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

class Screen_Creator:



class ArcadeEntrance(Screen):
	def __init__(self, world, camera):
		Screen.__init__(self, world, camera)
		self.create_rooms()

	def create_rooms(self):
		self.background = Backdrops('Arcade01')
		self.background.set_layer(1)
		self.chr = Clickable('Thomas01',800, 400, 'Thomas')
		#self.chr.image= pygame.transform.scale(self.chr.image, (int(self.chr.rect.width*0.7), int(self.chr.rect.height*0.7)))
		self.chr.set_layer(2)
		self.sg_all.add(self.background)
		self.sg_all.add(self.chr)
		self.sg_clickables.add(self.chr)
