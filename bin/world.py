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
		self.world = World
		self.camera        = Camera
		self.dialogs       = Dialog_Manager(self, self.world.script_manager.game_flags)
		self.sg_all        = pygame.sprite.LayeredUpdates()
		self.sg_clickables = pygame.sprite.LayeredUpdates()
		self.sg_dialogs    = pygame.sprite.LayeredUpdates()


	def update(self):
		self.dialogs.update()
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
		#self.dialog_manager = Dialog(self)
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


# Create separate dialog trees, thats separate from characters, give it a field for which character speaks it.
# Create a separate character json class. Why? IDK


class Dialog_Manager():
	def __init__(self, screen, game_flags):
		self.scene = screen
		self.game_flags = game_flags
		self.font = assets.load("Pixel_Font", 25)
		with open('bin/configs/dialog.json') as characters:
			self.dialogs = json.load(characters)
		self.sg_dialogs  = pygame.sprite.LayeredUpdates()

	def start_dialog(self, action):
		for dialogs in self.dialogs[action['character']]:
			DIALOG = self._has_required_flags(self.dialogs[action['character']][dialogs])
			print(DIALOG)
			if DIALOG != False:
				new_dialog = Dialog_Object(DIALOG['dialog'], self.font, action['character'])
				for sprites in self.scene.sg_all:
					if sprites.name == new_dialog.name:
						new_dialog.rect.centerx = sprites.rect.x 
						new_dialog.rect.y       = sprites.rect.y - 50

				self.sg_dialogs.add(new_dialog)
				self.scene.sg_all.add(new_dialog)

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


	def update(self):
		for dialogs in self.sg_dialogs:
			dialogs.start_dialog()





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
					print (actions)
					action = self._has_required_flags(actions)
					if action != False:
						if action['type'] == 'move':
							print("DEBUG: Moved To > ", action['dest'])
							self.world.set_screen(action['dest'])

						elif action['type'] == 'dialog_start':
							self.world.current_screen.dialogs.start_dialog(action)

						elif action['type'] == 'set_flag':
							self._set_flags(action['flag_settings'])

	def _set_flags(self, flag_settings):
		for flag in flag_settings:
			if flag in self.game_flags:
				print("DEBUG: Setting > ", flag, " > to >", flag_settings[flag])
				self.game_flags[flag] = flag_settings[flag]
			else:
				print("DEBUG: No Such Flag Called > ", flag)

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
	