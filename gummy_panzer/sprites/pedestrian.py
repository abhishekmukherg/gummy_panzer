import pygame
from . import util
from .. import settings

class Pedestrian(object):

	def __init__(self, species, animation, splatter, height, x):
        self.species = species         #species has two states. 0 is human. 1
                                       #is alien.
        self.animation = animation     #animation has four states. 0 is
                                       #standing/shooting. 1 is running left. 2
                                       #is running right. 3 is being beamed up.
        self.splatter = splatter        #splatter has two states. 0 is
                                        #unsplatted. 1 is splatted.
        self.depth = height           #depth to control which people appear
                                       #on top
		self.x = x
		pygame.sprite.Sprite.__init__(self)
		if species == 0:
			#human sprites
		elif species == 1:
			#alien sprites
		
	def beam_me_up(self):
		if self.splatter == 1:
			break
		elif self.animation == 3:
			break
		else:
			return 3
			
	def splat_me(self):
		if self.splatter == 1:
			break
		elif self.animation == 3:
			break
		else:
			if self.species == 0:
                #score = score - 5		#players could lose points for having
                                        #humans die. currently commented out
            return (1, self.depth + 20)     # return a value for splatter and a
                                             # modification for depth so that
                                             # blood always appears below
                                             # non-splattered
	
    def update(self):		#function to change the horizontal location of
                                #pedestrians
		if self.splatter == 1:
            self.x -=2 #function will return the distance to move the
                                #object to the left
		if self.animation == 1:
            self.x -=3 #returns a larger number for units that are
                                #running left
		if self.animation == 2:
			self.x -=1
		return -3
	
	def is_on_screen(self):
		if width + 4 =< screenleftside
			self.delete()
			
	def draw_person(self):
		if self.splatter == 1:
			return "filename"
		elif self.species == 0:
			if self.animation == 0:
				return "filename3"
			elif self.animation == 1:
				return "filename4"
			elif self.animation == 2:
				return "filename5"
			else self.animation == 3:
				return "filename6"
		else:
			if self.animation == 0:
				return "filename7"
			elif self.animation == 1:
				return "filename8"
			elif self.animation == 2:
				return "filename9"
			else self.animation == 3:
				return "filename10"

class Alien(Pedestrian):

	def __init__(self):
		Pedestrian.__init__(self)
				
class Human(Pedestrian):

	def __init__(self):
		Pedestrian.__init__(self)				
				
				
