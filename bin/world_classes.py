import pygame
from .asset_loader import Assets
from . import tools
assets = Assets()

class Sprite(pygame.sprite.Sprite):	
	def __init__(self,image, name = "Default"):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
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

class Characters(Sprite):
	def __init__(self, image, name):
		Sprite.__init__(self, image)
		self.name = name


class Dialog_Object(pygame.sprite.Sprite):
	def __init__(self, text_list, font, character_name):
		pygame.sprite.Sprite.__init__(self)
		self.name = character_name
		self.text_list = text_list
		self.create_text_sprites(font)
		self._inworld = True
		self.can_click = False
		self.cur_iter = 0
		self.max_wait = 90
		self.cur_wait = 0
		self._layer   = 20

	def create_text_sprites(self, font):
		self.image_list= []
		for texts in self.text_list:
			self.image_list.append(font.render(texts, True, pygame.Color('white'),(0, 0)))
			self.image = self.image_list[0]
			self.rect  = self.image.get_rect()

	def start_dialog(self):
		
		if self.max_wait == self.cur_wait:
			self.cur_iter = (self.cur_iter + 1) % len(self.image_list)
			old_centerx, old_y  = self.rect.centerx, self.rect.y
			self.image = self.image_list[self.cur_iter]
			self.rect  = self.image.get_rect()
			self.rect.centerx, self.rect.y = old_centerx, old_y
			self.cur_wait = 0

		else:
			self.cur_wait += 1
		if self.cur_iter == len(self.image_list) - 1:
			self.kill()






class FontSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self._inworld = False
		self.can_click = False

	def update(self):
		pass

	def set_layer(self, layer):
		self._layer = layer