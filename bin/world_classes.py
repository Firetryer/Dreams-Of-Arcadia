import pygame
from .asset_loader import Assets
from . import tools
assets = Assets()

class Sprite(pygame.sprite.Sprite):	
	def __init__(self,image):
		pygame.sprite.Sprite.__init__(self)
		self._inworld = True #Whether or not to convert coordinates to screen space
		self.can_click = True
		self.animation = Animation(self)
		self.set_image(image)

	def set_image(self, image):
		frames, self.MasterImage, name = assets.load(image)
		print(frames)
		self.image = frames[0]
		self.animation.add_animation(frames, name)
		self.rect = self.MasterImage.get_rect()
		self.animation.set_animation(name)
		
	def update(self):
		self.animation.loop_animation(self.image)

	def set_layer(self, layer):
		self._layer = layer
		#If something isn't render properly CHECK YOUR LAYERS
		

class Animation():
	def __init__(self, sprite):
		self.animation_list = {}
		self.current_animation = None
		self.current_iter = 0
		self.sprite = sprite
		self.delay_max = 10
		self.delay_cur = 0

	def add_animation(self, frames, name):
		self.animation_list[name] = frames

	def set_animation(self, name):
		self.current_animation = self.animation_list[name]

	def loop_animation(self, image):
		self.current_iter = (self.current_iter + 1) % len(self.current_animation)
		if self.delay_cur == self.delay_max:
			self.sprite.image = self.current_animation[self.current_iter]
			self.delay_cur = 0
		else:
			self.delay_cur += 1



class Backdrops(Sprite):
	def __init__(self, image):
		Sprite.__init__(self, image)
		self.rect.x = 0
		self.rect.y = 0



class Clickable(Sprite):
	def __init__(self, image, x = 0, y = 0, name = "Clicky"):
		Sprite.__init__(self, image)
		self.name = name
		self.rect.x = x
		self.rect.y = y


class FontSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self._inworld = False
		self.can_click = False

	def update(self):
		pass

	def set_layer(self, layer):
		self._layer = layer