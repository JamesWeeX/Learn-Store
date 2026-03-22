import pygame
from plant import Plant
from gameobject import ImageObject
from common import commonTool as t

class Scene(ImageObject):
	def __init__(self,background,layout):
		super().__init__()
		self.loadImgs(background)
		self.plantGroups = pygame.sprite.Group()
		self.bulletGroups = pygame.sprite.Group()
		self.zombieGroups = pygame.sprite.Group()
		self.uiGroups = pygame.sprite.Group()
		self.layout = layout
		self.pos[0] = -200

	def sceneEvent(self,event,mouse):
		self.enterEvent(event,mouse)
		self.exitEvent(event,mouse)
		self.buttonDownEvent(event,mouse)
		self.buttonUpEvent(event,mouse)
		self.moveEvent(event,mouse)

	def enterEvent(self,event,mouse):
		if event.type == pygame.MOUSEMOTION:
			for ui in self.uiGroups:
				ui.enterEvent(event,mouse)

	def exitEvent(self,event,mouse):
		if event.type == pygame.MOUSEMOTION:
			for ui in self.uiGroups:
				ui.exitEvent(event,mouse)

	def buttonDownEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONDOWN:
			for ui in self.uiGroups:
				ui.buttonDownEvent(event,mouse)

	def buttonUpEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONUP:
			for ui in self.uiGroups:
				ui.buttonUpEvent(event,mouse)

	def moveEvent(self,event,mouse):
		if event.type == pygame.MOUSEMOTION:
			for ui in self.uiGroups:
				ui.moveEvent(event,mouse)

	def update(self,current_time):
		for plant in self.plantGroups:
			bullet = plant.update(current_time)
			if bullet is not None:
				self.addBullet(bullet)
		for bullet in self.bulletGroups:
			bullet.update(current_time)
		for ui in self.uiGroups:
			ui.update(current_time)

	def draw(self,current_time):
		super().draw(self.layout,current_time)
		for bullet in self.bulletGroups:
			bullet.draw(self.layout,current_time)
		for plant in self.plantGroups:
			plant.draw(self.layout,current_time)
		for ui in self.uiGroups:
			ui.draw(self.layout,current_time)

	def addPlant(self,plant):
		self.plantGroups.add(plant)

	def addBullet(self,bullet):
		self.bulletGroups.add(bullet)
