import os,time,json
from functools import wraps


IMAGE_SRC = {}
OBJECT_XL = {}
OBJ_STATE_MAP = {}

def codeTime(func):
	@wraps(func)
	def runTime(*arg,**kwargs):
		star_time = time.time()
		func(*arg,**kwargs)
		end_time = time.time()
		execution_time = round((end_time - star_time)*1000,2)
		print(f"Function <{func.__name__}> executed in {execution_time} ms" )
	return runTime

def clmpValue(v,a,b):
	return min(max(v,a),b)

def isClmpValue(v,a,b):
	return clmpValue(v,a,b) == v

class Tool():
	def __init__(self):
		self.publicDirs = []
		self.publicPaths = {}

	def setpublicdirs(self,d):
		if os.path.isdir(d):
			self.publicDirs.append(d)

	def dir(self,name,file = True):
		for dr in self.publicDirs:
			for p in os.listdir(dr):
				path = os.path.join(dr,p)
				if not os.path.isdir(path) and file:
					na,ext = os.path.splitext(p)
					if na == name:
						return path
				else:
					if p == name:
						return path	
		
	def searchRoot(self,root):
		"""search dir from root"""
		dirs = []
		rootdir = os.path.join(root)
		dirs.append(rootdir)
		while len(dirs) > 0:
			ndir = dirs.pop()
			if os.path.isdir(ndir):
				self.setpublicdirs(ndir)
				ldir = os.listdir(ndir)
				for d in ldir:
					dirs.append(os.path.join(ndir,d))
			else:
				ls = ndir.split("\\")[-1].split(".")
				self.publicPaths[ls[0]] = ndir
				#print(ndir)

	def readJsonData(self,jsonfile):
		data = {}
		print(self.publicPaths)
		if jsonfile in self.publicPaths:
			filePath = self.publicPaths[jsonfile]
			f = open(filePath)
			data = json.load(f)
			f.close()
		return data

	def __call__(self,*arg,**kwargs):
		return self

commonTool = Tool()
commonTool.searchRoot('resources')
OBJ_STATE_MAP = commonTool.readJsonData('objectState')

print(f"OBJ_STATE_MAP:{OBJ_STATE_MAP}")

'''
gra = os.path.join('resources','graphics')
back = os.path.join('resources','graphics','Items','Background')
t.setpublicdirs(gra)
t.setpublicdirs(back)

a = t.dir('Background_0')
print(a)
'''
