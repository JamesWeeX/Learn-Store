from gameobject import ImageObject,UiObject
import pygame,random
import datatype  as dt

class Button(UiObject):
	def __init__(self,imagepath,pos):
		super().__init__()
		self.loadImgs(imagepath)
		self.type = dt.BUTTON_UI
		self.pos = pos	

	def update(self,current_time):
		super().update(current_time)		

	def draw(self,scene,current_time):
		super().draw(scene,current_time)

	def buttonDownEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONDOWN:
			super().buttonDownEvent(event,mouse)
			if self.getOpera(dt.EVENT_ENTER) and mouse['state'] == dt.DOWN_SYS:
				self.addOpera(dt.EVENT_DOWN)
				if self.type == dt.BUTTON_UI:
					self.alpha = 0
				if self.cleckedEvent is not None:
					self.cleckedEvent()

	def buttonUpEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONUP:
			super().buttonUpEvent(event,mouse)
			if self.getOpera(dt.EVENT_DOWN):
				self.removeOpera(dt.EVENT_DOWN)
				if self.type == dt.BUTTON_UI:
					self.alpha = 255

class Sun(Button):
	def __init__(self):
		self.pos = [random.randint(50,750),0]
		super().__init__('Sun',self.pos)
		self.objName = 'Sun'
		self.type = dt.SUN_UI
		self.timeNode = 0
		self.state = [0,len(self.imgs)]
		self.addMoneyEvent = None
	
	def update(self,current_time):
		if current_time - self.timeNode > 100:
			self.pos[1] += 10
		if self.pos[1] > 600:
			self.kill()

	def buttonUpEvent(self,event,mouse):
		super().buttonUpEvent(event,mouse)
		if event.type == pygame.MOUSEBUTTONUP and self.getOpera(dt.EVENT_ENTER):
			if self.addMoneyEvent is not None:
				self.addMoneyEvent()
			self.kill()

class Card(Button):
	def __init__(self,imagepath,pos,cost):
		super().__init__(imagepath,pos)
		self.type = dt.CARD_UI
		self.setScale([0.8,0.8])
		self.cost = cost
		self.using = False
		self.planting = False
		self.frozentime = 2000
		self.refreshtime = 0
		self.getgoldCallBack = None
		self.plantBeginCallBack = None
		self.plantEndCallBack = None

	def update(self,current_time):
		pass

	def frozentUpdate(self,current_time):
		#冷卻CD
		time = current_time - self.timeNode
		Index = self.imgIndex + self.state[0]
		if Index >= len(self.imgs):
			return None
		goldNum = 0
		if self.getgoldCallBack is not None:
			goldNum = self.getgoldCallBack()
		if time < self.frozentime:
			image = pygame.Surface([self.rect.w,self.rect.h])
			frozenimage = self.imgs[Index].copy()
			frozenimage.set_alpha(128)
			frozenheight = (self.frozentime - time)/self.frozentime * self.rect.h
			image.blit(frozenimage,(0,0),(0,0,self.rect.w,frozenheight))
			image.blit(self.imgs[Index],(0,frozenheight),
				(0,frozenheight,self.rect.w,self.rect.h - frozenheight))
		elif self.cost > goldNum:
			self.setAlpha(100)
			image = None
		else:
			image = self.imgs[Index] if Index < len(self.imgs) else None
		return image

	def buttonDownEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONDOWN:
			super().buttonDownEvent(event,mouse)
			if self.getOpera(dt.EVENT_DOWN):
				if not self.using:
					self.selected = not self.selected
				else:
					self.planting = not self.planting
					if self.planting and self.plantBeginCallBack is not None:
						self.plantBeginCallBack(self.objName)
					elif self.plantEndCallBack is not None:
						self.plantEndCallBack(mouse)


	def setAlpha(self,alpha):
		self.alpha = alpha

	def buttonUpEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONUP:
			super().buttonUpEvent(event,mouse)

	def clone(self,copy):
		copy = Card(self.objName,[0,0],self.cost)
		copy.objName = self.objName
		return copy

	def draw(self,scene, current_time):
		super().draw(scene,current_time)
		if self.using:
			image = self.frozentUpdate(current_time)
			if image is not None:
				rel_image = self.updateScale(image)
				self.blit_alpha(scene,rel_image,self.pos,self.alpha)

class Menu(UiObject):
	def __init__(self,imagepath,pos):
		super().__init__()
		self.loadImgs(imagepath)
		self.type = dt.MENU_UI
		self.pos = pos