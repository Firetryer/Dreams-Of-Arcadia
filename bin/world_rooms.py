from .world import *

class ArcadeEntrance(Screen):
	def __init__(self, world, camera):
		Screen.__init__(self, world, camera)
		self.create_rooms()

	def create_rooms(self):
		self.background = Backdrops('Arcade01')
		self.background.set_layer(1)
		self.chr = Clickable('Thomas01',800, 400, 'Thomas')
		#self.chr.image= pygame.transform.scale(self.chr.image, (int(self.chr.rect.width*0.7), int(self.chr.rect.height*0.7)))
		self.chr.set_layer(2)
		self.sg_all.add(self.background)
		self.sg_all.add(self.chr)
		self.sg_clickables.add(self.chr)
