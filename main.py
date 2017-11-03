import pygame
from bin import GAME
import json

class Game:
	def __init__(self):
		pygame.init()
		self.GAME = True
		with open("bin/settings.json") as settings:
			settings = json.load(settings)

		self.screen = pygame.display.set_mode((settings['resolution']['x'], settings['resolution']['y']))
		self.clock = pygame.time.Clock()
		self.game = GAME.GameManager()
		self.game_loop()

	def game_loop(self):
		
		while self.game_loop:
			current_time = self.clock.tick()
			self.screen.fill([0, 0, 0])
			self.game.update()
			self.game.render(self.screen)
			for event in pygame.event.get():

				self.game.handle_events(event)

				if event.type == pygame.QUIT:
					self.game_loop = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.game_loop = False
			pygame.display.flip()


		pygame.quit()