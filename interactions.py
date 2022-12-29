#here will be stored classes of objects we can click on
import pygame

tile_size=40

#class with our doors
class Door(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/doors.png')
		self.image = pygame.transform.scale(img, (tile_size*3, tile_size*5))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#class to backdoors
class BackDoor(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/backdoors.png')
		self.image = pygame.transform.scale(img, (tile_size*3, tile_size*5))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#patient card
class PatientCard(pygame.sprite.Sprite):
	def __init__(self, x, y,z):
		pygame.sprite.Sprite.__init__(self)
		img=pygame.image.load('img/patientCard.png')
		if z==1:
			self.image = pygame.transform.scale(img, (tile_size//2, tile_size)) #show in game collectible item
		elif z==2:
			self.image=pygame.transform.scale(img, (tile_size*10, tile_size*18)) #show in inventory, in readable size
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y