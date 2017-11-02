import pygame
import json

class Assets:
	def __init__(self):
		with open("bin/settings.json") as settings:
			self.settings = json.load(settings)

		with open('bin/assets.json') as assets:
			self.assets = json.load(assets)

	def load(self, name):
		reso = self.settings['resolution']
		print(reso)
		image = pygame.image.load(self.assets[name]).convert_alpha()
		if reso['x'] < 1920 and reso['y'] < 1080:
			offset_width  = reso['x'] / 1920 * 100			
			offset_height = reso['y'] / 1080 * 100
		print (image.get_rect().x, image.get_rect().y)
		image = pygame.transform.scale(image, (int(image.get_rect().width * (offset_width / 100)), int(image.get_rect().height * (offset_height/100))))

		print(offset_height, offset_width)
		return image
