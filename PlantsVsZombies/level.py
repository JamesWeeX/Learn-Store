from scene import Scene
from ui import Card,Menu,Button,Sun
from common import commonTool as t
import datatype  as dt
import plant as p
import pygame,copy

class Level(Scene):
	def __init__(self,level_data_json,layout):
		self.data = t.readJsonData(level_data_json)
		super().__init__(self.data['Background'],layout)
		self.OPERA = 0                 #通关或失败
		self.initData()
		self.enableCards = []
		self.timeNode = 0
		self.goldNum = 0
		self.planobj = None

	def addGold(self):
		self.goldNum = self.goldNum + 30

	def getGoldNum(self):
		return self.goldNum

	def plantBegin(self,Name):
		if Name == 'card_peashooter':
			self.planobj = p.ShowPea()
		#elif Name == '':
		print(f"create {Name}")
		self.addPlant(self.planobj)

	def planEnd(self,mouse):
		if mouse['pos'][1] < 80:
			self.planobj.kill()
			print(f"planobj {self.planobj}")
			self.planobj = None

	def drawScene(self):
		for y in range(1,8):
			for x in range(1,12):
				pygame.draw.line(self.layout,(255,0,0),[x*80,0],[x*80,600],1)
				pygame.draw.line(self.layout,(0,255,0),[0,y*80+15],[800,y*80+15],1)

	def update(self,current_time):
		super().update(current_time)
		if self.OPERA == 2 and current_time - self.timeNode >1000:
			self.timeNode = current_time
			sun = Sun()
			sun.addMoneyEvent = self.addGold
			self.uiGroups.add(sun)

	def buttonDownEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONDOWN:
			super().buttonDownEvent(event,mouse)
			for card in self.uiGroups:
				if card.type == dt.CARD_UI and self.OPERA == 1:
					if card.selected and len(self.enableCards) < 8 and not len([c for c in self.enableCards if card.objName == c.objName]):
						card.setAlpha(125)
						newcard = None
						newcard = card.clone(newcard)
						self.enableCards.append(newcard)
					elif not card.selected:
						card.setAlpha(255)
						for c in self.enableCards:
							if card.objName == c.objName:
								self.enableCards.remove(c)
				elif card.type == dt.BUTTON_UI:
					pass

	def buttonUpEvent(self,event,mouse):
		if event.type == pygame.MOUSEBUTTONUP:
			super().buttonUpEvent(event,mouse)

	def moveEvent(self,event,mouse):
		if self.planobj is not None:
			rect = self.planobj.rect
			x = mouse['pos'][0] - rect[2]/2
			y = mouse['pos'][1] - rect[3]/2
			self.planobj.pos = [x,y]
			

	def drawCardMenu(self,current_time):
		menupos = [80,6]
		offset = 53
		cardNum = 0
		for card in self.enableCards:
			card.pos[0] = menupos[0] + cardNum*offset
			card.pos[1] = menupos[1]
			card.draw(self.layout,current_time)
			cardNum = cardNum + 1

	def draw(self,current_time):
		super().draw(current_time)
		self.drawCardMenu(current_time)
		self.drawScene()
		img = self.getSunValueImage(self.goldNum)
		if img is not None:
			self.layout.blit(img,(20,63))

	def initData(self):
		menudata = self.data['menus']
		for name, pos in menudata.items():
			m = Menu(name,pos)
			m.objName = name
			self.uiGroups.add(m)
		buttons = self.data['button']
		for name, pos in buttons.items():
			b = Button(name,pos)
			b.objName = name
			b.cleckedEvent = lambda : self.beginPlay()
			self.uiGroups.add(b)
		carddata = self.data['cardgroup']
		cardNum = 0
		rowNum = 8
		pos = [22, 130]
		offset = [53 , 73]
		for name,cost in carddata.items():
			img_pos = [0,0] 
			img_pos[0] = pos[0] + offset[0]*int(cardNum % rowNum)
			img_pos[1] = pos[1] + offset[1]*int(cardNum / rowNum)
			c = Card(name,img_pos,cost)
			c.objName = name
			self.uiGroups.add(c)
			cardNum = cardNum + 1

	def beginPlay(self):
		self.OPERA = 2
		for card in self.uiGroups:
			if card.type == dt.CARD_UI or card.type == dt.BUTTON_UI or card.objName == 'PanelBackground':
				self.uiGroups.remove(card)
		for card in self.enableCards:
			card.getgoldCallBack = lambda : self.getGoldNum()
			card.plantBeginCallBack = lambda n: self.plantBegin(n)
			card.plantEndCallBack = lambda p: self.planEnd(p)
			card.using = True
			card.timeNode = pygame.time.get_ticks()
			self.uiGroups.add(card)

	def getSunValueImage(self,sun_value):
		font = pygame.font.SysFont(None, 22)
		width = 32
		msg_image = font.render(str(sun_value), True, ( 60,  60, 100), (234, 233, 171))
		msg_rect = msg_image.get_rect()
		msg_w = msg_rect.width
		image = pygame.Surface([width, 17])
		x = width - msg_w
		image.fill((234, 233, 171))
		image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
		image.set_colorkey((  0,   0,   0))
		return image


