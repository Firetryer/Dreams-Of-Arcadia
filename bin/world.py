import pygame
from .world_classes import *
from . camera import Camera
from . import tools
from . import world_rooms
import json


class Screen:
	def __init__(self, World, Camera):
		self.name = None
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


class World:
	def __init__(self):
		self.camera = Camera()
		self.screen_manager = Screen_Manager(self, self.camera)
		self.set_screen('arcade')

	def set_screen(self, newscreen):
		self.current_screen = self.screen_manager.get_scene(newscreen)

	def update(self):
		self.current_screen.update()

	def render(self, screen):
		self.current_screen.render(self.camera, screen)
		

	def handle_events(self, event):
		self.current_screen.handle_events(event)


#Create screens if its not already made, else load from self.scenes
class Screen_Manager:
	def __init__(self, World, Camera):

		self.world = World
		self.camera = Camera

		with open('bin/configs/world_locations.json') as location:
			self.scene_configs = json.load(location)
		
		self.scenes = {}

	def create_scenes(self, name):
		scene_data = self.scene_configs[name]

		#Initialize New Scene
		new_scene = Screen(self.world, self.camera)
		new_scene.name = scene_data['name']
		#Add Background to Scene
		background = Backdrops(scene_data['background'])
		background.set_layer(1)
		new_scene.sg_all.add(background)

		#interactables
		for sprites in scene_data['interactables']:
			#THIS IS IMPORTANT IF SOMETHING GOES WRONG RELATED TO THIS, CHECK HERE
			sprite=scene_data['interactables'][sprites]
			new_sprite = Clickable(sprite['image'],sprite['location']['x'],sprite['location']['y'],sprites)
			#END OF IMPORTANT STUFF
			new_sprite.action = sprite['action']
			new_scene.sg_all.add(new_sprite)
			new_scene.sg_clickables.add(new_sprite)
		self.scenes[name]=new_scene

	def get_scene(self, name):
		if name not in list(self.scenes):
			self.create_scenes(name)

		return self.scenes[name]


class Dialog_Manager():
	def __init__(self):
		pass