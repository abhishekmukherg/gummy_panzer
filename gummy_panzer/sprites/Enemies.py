
import pygame
from . import EnemyInfo
#from .sprites import util

class aerialEnemy(object):

    def __init__(self,sprite,x,y,speed=1,strength=1,pat_step=0):
        if sprite = ENEMY_SPRITE_ONE:
            pass
        elif sprite = ENEMY_SPRITE_TWO:
            pass
        elif sprite = ENEMY_SPRITE_THREE:
            pass
        else:
            del self

        self.x = x
        self.y = y
        self.pat_step = pat_step
        
        self.image = load_image(sprite)
    
    def update(self):
        self.x = self.speed * self.pattern[pat_step][0]
        self.y = self.speed * self.pattern[pat_step][1]
        pat_step++
        if pat_step = len(pattern):
            pat_step = 0