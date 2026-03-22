from gameobject import ImageObject
from common import codeTime
from bullet import PeaBullet
import pygame
import common as c

class Plant(ImageObject):
	"""plant base"""
	def __init__(self):
		super().__init__()
		self.planTimeNode = pygame.time.get_ticks()
		self.healValue = 100

	def attack(self):
		pass

class ShowPea(Plant):
	def __init__(self):
		super().__init__()
		super().initStateMap('SnowPea')
		super().loadImgs('SnowPea')
		super().setState('Normal')
		self.shooting = False

	def attack(self):	
		bullet = PeaBullet()
		bullet.pos = [self.pos[0] + self.size[0]/2,self.pos[1]]	
		return bullet

	def update(self,current_time):
		bullet = None
		if self.frameEnd:
			if self.stateKey == 'Attack':
				super().setState('Normal')
				bullet = self.attack()
		if current_time - self.planTimeNode > 5000:		
			super().setState('Attack')
			self.planTimeNode = current_time			
		return bullet

	def draw(self,scene,current_time):
		super().draw(scene,current_time)
		