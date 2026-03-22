import pygame
from gameobject import ImageObject


class Bullet(ImageObject):
	"""Bullet"""
	def __init__(self):
		super().__init__()
		self.speed = 4
		self.createTimeNode = pygame.time.get_ticks()

	def update(self,current_time):
		if current_time - self.createTimeNode > 20:
			self.pos[0] = self.pos[0] + self.speed
			self.createTimeNode = current_time
		if self.frameEnd:
			if self.stateKey == 'Destory':
				a = self.kill()
		if(self.pos[0] > 500):
			super().setState('Destory')
			self.speed = 0

class PeaBullet(Bullet):
	def __init__(self):
		super().__init__()
		super().initStateMap("PeaBullet")
		super().loadImgs('PeaNormal')
		super().loadImgs('PeaNormalExplode')
		super().setState('Normal')
		self.objName = "PeaBullet"

	def update(self,current_time):
		super().update(current_time)
		if self.frameEnd:
			self.playspeed = 200
			self.imgIndex = 0