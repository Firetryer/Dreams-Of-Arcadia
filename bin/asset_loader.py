import pygame
import json
from . import tools

class Assets:
	def __init__(self):

		with open('bin/configs/assets.json') as assets:
			self.assets = json.load(assets)

	def load_font(self, name, size):
		print("DEBUG: ", name, " == ", self.assets[name]['file'], " == ", tools.size_to_screen(size))
		MasterFont = pygame.font.Font(self.assets[name]['file'], tools.size_to_screen(size))
		return MasterFont


	def load_image(self, name, scale=True):
		MasterImage = pygame.image.load(self.assets[name]['file'])
		image = MasterImage
		if scale:
			image = self.scale_image(MasterImage)
		return [image], MasterImage, name

	def load_animation(self, name, scale = True):
		with open(self.assets[name]['info']) as info:
			sheets = json.load(info)
		single = sheets['frames'][0]['frame'] # Get a single frame for use as master image
		frames = []
		SpriteSheet_Master = pygame.image.load(self.assets[name]['file'])
		Sprite_Master = SpriteSheet_Master.subsurface(pygame.Rect(single['x'], single['y'], single['w'], single['h']))

		
		iterate = 0
		for frame in sheets['frames']:
			z = frame['frame']
			new_frame = SpriteSheet_Master.subsurface(pygame.Rect(z['x'], z['y'], z['w'], z['h']))
			self.scale_image(new_frame)
			frames.append(new_frame)

		print(frames, Sprite_Master)
		return frames, Sprite_Master, name

	def load(self, name, size = 5, scale = True):
		
		if name in self.assets:
			file = self.assets[name]
		else:
			print("DEBUG: ERROR NO FILE CALLED > ", name)
			return self.load_image('DEFAULT')
			
		if file['type'] == 'animated':
			return self.load_animation(name)
		elif file['type'] == 'static':
			return self.load_image(name)
		elif file['type'] == 'font':
			if size == 5:
				print("DEBUG: FONT Size is default 5")
			return self.load_font(name, size)

	def scale_image(self, master_image):
		w, h = master_image.get_rect().width, master_image.get_rect().height
		image = pygame.transform.scale(master_image, tools.world_to_screen(w, h))
		return image

