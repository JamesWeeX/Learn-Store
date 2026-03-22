import pygame,os
import common as c
import datatype  as dt
from common import commonTool as t
from common import isClmpValue

class ImageObject(pygame.sprite.Sprite):
	"""
	ImageAnima Base
	state (start_index,end_index)
	"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.stateMap = {'Select':[0,0], 'Normal':[0,0]}
		self.stateKey = 'Normal'
		self.alpha = 255
		self.imgs = []
		self.pos = [0, 0]
		self.state = [0, 0]  
		self.size = [1, 1]
		self.scale = [1, 1]  
		self.timeNode = 0.0 
		self.imgIndex = 0
		self.playspeed = 100
		self.frameEnd = False
		self.objName = None
		self.rect = [0,0,0,0]

	def loadImgs(self,directoryName):
		"""load all Imgs"""
		if directoryName in c.OBJECT_XL:
			for name in c.OBJECT_XL[directoryName]:
				self.imgs.append(c.IMAGE_SRC[name])
		else:
			objectXl = []
			directory = t.dir(directoryName)
			if os.path.isdir(directory):                        #this t.dir() spend long time.
				for name in os.listdir(directory):
					path = os.path.join(directory,name)
					if not os.path.isdir(path):
						self.imgs.append(pygame.image.load(path).convert())
						color = self.imgs[-1].get_at((0,0))
						self.imgs[-1].set_colorkey(color,pygame.RLEACCEL)
						c.IMAGE_SRC[name] = self.imgs[-1]						
						objectXl.append(name)
			else:
				self.imgs.append(pygame.image.load(directory).convert())
				c.IMAGE_SRC[directoryName] = self.imgs[-1]
				objectXl.append(directoryName)
			c.OBJECT_XL[directoryName] = objectXl

	def initStateMap(self,objectName):
		#print(f"<init_before> {str(objectName)} from {c.OBJ_STATE_MAP} onin {str(objectName) in c.OBJ_STATE_MAP}")
		if str(objectName) in c.OBJ_STATE_MAP:
			self.stateMap = c.OBJ_STATE_MAP[objectName]
			#print(f"<init_after> {objectName} {self.stateMap}")

	def setState(self,strkey):
		#print(f"before {strkey} | {self.stateMap}")
		if strkey in self.stateMap:
			curIndex = self.imgIndex + self.state[0]
			self.state = self.stateMap[strkey]
			self.stateKey = strkey
			self.imgIndex = 0

	def setScale(self,scale):
		self.scale = scale

	def blit_alpha(self,target,source,pos,opacity):
		x = pos[0]
		y = pos[1]
		temp = pygame.Surface((source.get_width(),source.get_height())).convert()
		temp.blit(target,(-x,-y))
		temp.blit(source,(0,0))
		temp.set_alpha(opacity)
		target.blit(temp,pos)

	def updateScale(self,org_img):
		self.rect = org_img.get_rect()
		img_w = self.rect[2] * self.scale[0]
		img_h = self.rect[3] * self.scale[1]
		rel_image = pygame.transform.scale(org_img,(img_w,img_h))
		return rel_image 

	def draw(self,scene,current_time):
		Index = self.imgIndex + self.state[0]
		if current_time - self.timeNode > self.playspeed:
			regon = self.state[1] - self.state[0]
			if self.state[1] - self.state[0] != 0:
				self.imgIndex = (self.imgIndex + 1)%regon
				self.timeNode = current_time
				self.size[0],self.size[1] = self.imgs[Index].get_size()
		rel_image = self.updateScale(self.imgs[Index])
		#scene.blit(rel_image,self.pos)
		self.blit_alpha(scene,rel_image,self.pos,self.alpha)
		self.frameEnd = self.imgIndex == 0 and current_time == self.timeNode

	def update(self,current_time):
		pass

class UiObject(ImageObject):
	def __init__(self):
		super().__init__()
		self.opera = 0
		self.type = dt.BASE_UI
		self.selected = False
		self.clecked = False
		self.cleckedEvent = None

	def moveEvent(self,event,mouse):
		pass

	def buttonDownEvent(self,event,mouse):
		pass

	def buttonUpEvent(self,event,mouse):
		pass

	def inner(self,cur_pos):
		bX = isClmpValue(cur_pos[0], self.pos[0], self.pos[0]+self.rect[2]*self.scale[0])
		bY = isClmpValue(cur_pos[1], self.pos[1], self.pos[1]+self.rect[3]*self.scale[1])
		return bX and bY

	def addOpera(self,opera):
		self.opera |= opera

	def removeOpera(self,opera):
		self.opera &= ~opera

	def getOpera(self,opera):
		return self.opera & opera

	def enterEvent(self,event,mouse):
		bCurInner = self.inner(mouse['pos'])
		bPerinner = self.inner(mouse['per'])
		if bPerinner == False and bCurInner == True:
			self.addOpera(dt.EVENT_ENTER)

	def exitEvent(self,event,mouse):
		bCurInner = self.inner(mouse['pos'])
		bPerinner = self.inner(mouse['per'])
		if bPerinner == True and bCurInner == False:
			self.removeOpera(dt.EVENT_ENTER)