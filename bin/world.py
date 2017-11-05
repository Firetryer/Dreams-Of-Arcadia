import pygame
from .world_classes import *
from . camera import Camera
from . import tools
from .asset_loader import Assets
from . import world_rooms
import json

assets = Assets()

class Screen:
	def __init__(self, World, Camera):
		self.name = None
		self.camera = Camera
		self.sg_all        = pygame.sprite.LayeredUpdates()
		self.sg_clickables = pygame.sprite.LayeredUpdates()
		self.sg_dialogs    = pygame.sprite.LayeredUpdates()

	def update(self):
		self.sg_all.update()

	def render(self,camera,screen):
		camera.display(screen, self.sg_all)

	def handle_events(self, event):
		#Add a focus blah blah blah
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()
			
			if bool(self.sg_dialogs):
				pos = (x,y)
				for sprites in self.sg_dialogs:
					if sprites.rect.collidepoint(pos) and sprites.can_click:
						return sprites
			else:
				pos = tools.screen_to_world(x,y)
				for sprites in self.sg_clickables:
					if sprites.rect.collidepoint(pos) and sprites.can_click:
						return sprites



class World:
	def __init__(self):
		self.camera = Camera()
		self.screen_manager = Screen_Manager(self, self.camera)
		self.script_manager = Scripting(self, self.screen_manager)
		self.dialog_manager = Dialog(self)
		self.current_screen = None
		self.set_screen('arcade')

	def set_screen(self, newscreen):
		self.current_screen = self.screen_manager.get_scene(newscreen)

	def update(self):
		self.current_screen.update()

	def render(self, screen):
		self.current_screen.render(self.camera, screen)
		

	def handle_events(self, event):
		self.script_manager.handle_click_events(self.current_screen.handle_events(event))


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
			if sprite['type'] == 'character':
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

# Next work on action system
# Work on dialog closing
# 

class Dialog():
	def __init__(self,World):
		self.world = World
		self.font = assets.load_font("Hack_Font", 25)
		with open('bin/configs/characters.json') as characters:
			self.dialogs = json.load(characters)
		self.character = None

	def StartDialog(self, action):
		self.character = self.dialogs[action['character']]
		self._StartDialog(action)

	def _StartDialog(self, action):
		dialogs   = self.character["dialogs"]
		sg_dialogs = pygame.sprite.LayeredUpdates()
		w, h = pygame.display.get_surface().get_size()
		#Add NPC Text
		for i in self._create_text_sprites(dialogs[action["dialog_id"]]["text"], (h/2/2)):
			sg_dialogs.add(i)
		
		#Add Options
		temp_list = []
		current_iter = 0
		for i in dialogs[action["dialog_id"]]["options"]:
			current_iter+=15
			temp_list.append(i)
			for z in self._create_text_sprites(dialogs[action["dialog_id"]]["options"][i]['text'], (h/2+current_iter*2), True):
				print(z.rect)
				z.action = dialogs[action['dialog_id']]['options'][i]['action']
				sg_dialogs.add(z)

		for texts in sg_dialogs:
			self.world.current_screen.sg_dialogs.add(texts)
			self.world.current_screen.sg_all.add(texts)
		

	def _create_text_sprites(self, text, y, clickable = False):
		print(text)
		w, h = pygame.display.get_surface().get_size()
		sg_dialogs = pygame.sprite.LayeredUpdates()
		line_number = y
		layer_order = 10
		first = True
		for lines in text:
			line_number += 36
			layer_order += 1
			new_line = FontSprite()
			if first:
				text_line_image = assets.load_image("text_lines", False)[0]
				first = False
			else:
				text_line_image = assets.load_image("text_lines_bottom", False)[0]
			text_line_image.blit(self.font.render(lines, True, pygame.Color('white')), (20,-1))
			new_line.image = text_line_image
			new_line.rect  = new_line.image.get_rect()
			new_line.rect.x = w/2/2
			new_line.rect.y = line_number
			#print(new_line.rect)
			if clickable:
				new_line.can_click = True
			new_line.set_layer(layer_order + 1)
			sg_dialogs.add(new_line)

		return sg_dialogs



	def next_dialog(self, action):
		self.exit_dialog()
		self._StartDialog(action)


	def exit_dialog(self):
		for sprites in self.world.current_screen.sg_dialogs:
			sprites.kill()

class Scripting():
	def __init__(self, World, manager):
		self.world = World
		self.manager = manager
		with open('bin/configs/game_flags.json') as flags:
			self.game_flags = json.load(flags)

	def handle_click_events(self,sprite):

		if sprite != None:
			if bool(sprite.action):
				for actions in sprite.action:
					action = self._has_required_flags(sprite.action[actions])
					print(sprite)

					if action != False:
						if action['type'] == 'move':
							print("moved to ", action['dest'])
							self.world.set_screen(action['dest'])
						elif action['type'] == 'dialog_start':
							self.world.dialog_manager.StartDialog(action)

						elif action['type'] == 'next_dialog':
							self.world.dialog_manager.next_dialog(action)

						elif action['type'] == 'exit_dialog':
							self.world.dialog_manager.exit_dialog()

	def _has_required_flags(self, action):
		#Check if has necessary flags required:
		if bool(action['flags_required']): #Is not empty
			for game_flags in self.game_flags:
				for required_flags in action['required_flags']:
					if game_flags == required_flags: #Checks if keys are the same
						#Checks if values are the same
						if self.game_flags[game_flags] == action['required_flags'][required_flags]: 
							print("DEBUG: VALUES ARE EQUAL")
							return action
						else:
							print("DEBUG: Values not equal")
							return False
							
		else:#No Requirements
			print("DEBUG: NO REQUIREMENTS")
			return action
	