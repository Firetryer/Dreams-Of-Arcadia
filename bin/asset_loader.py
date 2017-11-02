import pygame
import json

class Assets:
	def load(name):
		with open('bin/assets.json') as assets:
			assets = json.load(assets)
		return pygame.image.load(assets[name]).convert_alpha()
