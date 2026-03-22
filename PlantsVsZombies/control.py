import pygame,sys,os,time
from scene import Scene
from pygame.locals import *
from plant import ShowPea
from common import codeTime
from level import Level
import datatype  as dt

sys_mouse = {
   'pos': [0,0],
   'per': [0,0],
   'v' : '',                 #button Value
   'state': dt.NONE_SYS,
   'flov' : 0.0}
sys_key = {
   'v' : '',
   'state' : dt.NONE_SYS}

class Control():
	def __init__(self):
		self.init()
		self.levelscene = None
		self.level = 0

	def init(self):
		pygame.init()
		pygame.display.set_caption("PlantVsZomblie")
		self.SCENE = pygame.display.set_mode((800,600))

	def eventLoop(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				sys_key['state'] = dt.DOWN_SYS		
			elif event.type == KEYUP:
				sys_key['state'] = dt.UP_SYS	
			elif event.type == MOUSEBUTTONDOWN:
				sys_mouse['state'] = dt.DOWN_SYS
				sys_mouse['per'] = sys_mouse['pos']
				sys_mouse['pos'] = pygame.mouse.get_pos()
				sys_mouse['v'] = pygame.mouse.get_pressed(3)
			elif event.type == MOUSEBUTTONUP:
				sys_mouse['state'] = dt.UP_SYS
				sys_mouse['per'] = sys_mouse['pos']
				sys_mouse['pos'] = pygame.mouse.get_pos()
				sys_mouse['v'] = pygame.mouse.get_pressed(3)
			elif event.type == MOUSEMOTION:
				sys_mouse['state'] = dt.NONE_SYS
				sys_mouse['per'] = sys_mouse['pos']
				sys_mouse['pos'] = pygame.mouse.get_pos()
				sys_mouse['v'] = pygame.mouse.get_pressed(3)
			if self.levelscene is not None:
				self.levelscene.sceneEvent(event,sys_mouse)

	def levelProcess(self):
		if self.levelscene is None or self.levelscene.OPERA == 0:
			levelName = f"level{self.level}" 
			self.levelscene = Level(levelName,self.SCENE)
			self.level = self.level + 1
			self.levelscene.OPERA = 1
			pea = ShowPea()
			pea.pos = [600,100]
			self.levelscene.addPlant(pea)

	#@codeTime		
	def render(self):
		current_time = pygame.time.get_ticks()
		self.eventLoop()
		if self.levelscene is not None:
			self.levelscene.update(current_time)
			self.levelscene.draw(current_time)
		pygame.display.update()

	def run(self):
		'''sp = ShowPea()
		self.scene = Scene('Background',self.SCENE)
		self.scene.addPlant(sp)
		sp.pos=[100,150]'''
		while True:
			self.levelProcess()
			self.render()

c = Control()	