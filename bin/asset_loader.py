import pygame
import json
from . import tools

class Assets:
	def __init__(self):

		with open('bin/configs/assets.json') as assets:
			self.assets = json.load(assets)

	def load(self, name):
		
		MasterImage = pygame.image.load(self.assets[name])
		w, h = MasterImage.get_rect().width, MasterImage.get_rect().height
		image = pygame.transform.scale(MasterImage, tools.world_to_screen(w, h))
		return image, MasterImage
