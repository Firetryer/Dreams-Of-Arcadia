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
			pos = tools.screen_to_world(x,y)
			for sprites in self.sg_clickables:
				if sprites.rect.collidepoint(pos):
					print("CLICKED: ", sprites.name)
					return sprites



class World:
	def __init__(self):
		self.camera = Camera()
		self.screen_manager = Screen_Manager(self, self.camera)
		self.scripts = Scripting(self, self.screen_manager)
		self.set_screen('arcade')

	def set_screen(self, newscreen):
		self.current_screen = self.screen_manager.get_scene(newscreen)

	def update(self):
		self.current_screen.update()

	def render(self, screen):
		self.current_screen.render(self.camera, screen)
		

	def handle_events(self, event):
		self.scripts.handle_click_events(self.current_screen.handle_events(event))


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

		#SPRITES
		for items in scene_data['interactables']:
			#THIS IS IMPORTANT IF SOMETHING GOES WRONG RELATED TO THIS, CHECK HERE
			sprite = scene_data['interactables'][items]
			if sprite['type'] == 'sprite':
				new_sprite = Clickable(sprite['image'],sprite['location']['x'],sprite['location']['y'],items)
				new_sprite.set_layer(3)

			elif sprite['type'] == 'mask':
				new_sprite = Clickable("Mask",sprite['location']['x'],sprite['location']['y'],items)
				new_sprite.rect.width, new_sprite.rect.height = sprite['location']['width'], sprite['location']['height']
				new_sprite.set_layer(4)

			new_sprite.action = sprite['action']
			new_scene.sg_all.add(new_sprite)
			new_scene.sg_clickables.add(new_sprite)

			
		self.scenes[name]=new_scene

	def get_scene(self, name):
		if name not in list(self.scenes):
			self.create_scenes(name)

		return self.scenes[name]


class Scripting():
	def __init__(self, World, manager):
		self.world = World
		self.manager = manager
		with open('bin/configs/game_flags.json') as flags:
			self.game_flags = json.load(flags)

	def handle_click_events(self,sprite):

		if sprite != None:
			print(sprite)
			action = self._has_required_flags(sprite) 
			if action != False:
				print(action)


	def _has_required_flags(self, sprite):
		#Check if has necessary flags required:
		if bool(sprite.action):#Is not empty
			print("DEBUG: NOT EMPTY")
			for actions in sprite.action: #Open Door
				if bool(sprite.action[actions]['flags_required']): #Is not empty
					for game_flags in self.game_flags:
						for required_flags in sprite.action[actions]['required_flags']:
							if game_flags == required_flags: #Checks if keys are the same
								#Checks if values are the same
								if self.game_flags[game_flags] == sprite.actions[actions]['required_flags'][required_flags]: 
									print("DEBUG: VALUES ARE EQUAL")
									return sprite.action[actions]
								else:
									print("DEBUG: Values not equal")
									return False
									
				else:#No Requirements
					print("DEBUG: NO REQUIREMENTS")
					return sprite.action[actions]
	