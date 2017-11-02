import pygame
from bin import GAME


class Game:
	def __init__(self):
		pygame.init()
		self.GAME = True
		self. screen = pygame.display.set_mode((1280, 720))
		self.clock = pygame.time.Clock()
		self.game = GAME.GameManager()
		self.game_loop()
	def game_loop(self):
		
		while self.game_loop:
			current_time = self.clock.tick()
			self.game.update()
			self.game.render(screen)
			self.game.handle_events()
			for events in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_loop = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.game_loop = False