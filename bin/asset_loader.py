import pygame
import json
from . import tools

class Assets:
	def __init__(self):

		with open('bin/configs/assets.json') as assets:
			self.assets = json.load(assets)

	def load_image(self, name, scale=True):
		
		MasterImage = pygame.image.load(self.assets[name])
		image = MasterImage
		if scale:
			image = self.scale_image(MasterImage)
		return image, MasterImage

	def scale_image(self, master_image):
		w, h = master_image.get_rect().width, master_image.get_rect().height
		image = pygame.transform.scale(master_image, tools.world_to_screen(w, h))
		return image

	def load_font(self, name, size):
		MasterFont = pygame.font.Font(self.assets[name], size)
		return MasterFont
