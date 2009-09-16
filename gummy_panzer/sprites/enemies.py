
import pygame
from . import EnemyInfo
#from .sprites import util

ENEMY_PATTERN_STRAIGHT = [(5,0)]
ENEMY_PATTERN_WAVE_MID_DOWN = [(-2,5),(-2,4),(-2,3),(-2,2),(-2,1),(-2,0),(-2,0),(-2,-1),(-2,-2),(-2,-3),(-2,-4),(-2,-5),(-2,-5),(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),(-2,5)]
ENEMY_PATTERN_WAVE_MID_UP = [(-2,-5),(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),(-2,5),(-2,5),(-2,4),(-2,3),(-2,2),(-2,1),(-2,0),(-2,0),(-2,-1),(-2,-2),(-2,-3),(-2,-4),(-2,-5)]
ENEMY_PATTERN_WAVE_TOP = [(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),(-2,5),(-2,5),(-2,4),(-2,3),(-2,2),(-2,1),(-2,0),(-2,0),(-2,-1),(-2,-2),(-2,-3),(-2,-4),(-2,-5)(-2,-5),(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0)]
ENEMY_PATTERN_WAVE_BOTTOM = [(-2,0),(-2,-1),(-2,-2),(-2,-3),(-2,-4),(-2,-5)(-2,-5),(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),(-2,5),(-2,5),(-2,4),(-2,3),(-2,2),(-2,1),(-2,0)]
ENEMY_PATTERN_DIAG_DOWN = [(-4,2)]
ENEMY_PATTERN_DIAG_UP = [(-4,-2)]

class aerialEnemy(object):

    def __init__(self,sprite,x,y,pat_step=0):
        if sprite = ENEMY_SPRITE_ONE:
            self.speed = 2
            self.strength = 1
            #self.points = 
            #self.pattern = ENEMY_PATTERN_STRAIGHT
        elif sprite = ENEMY_SPRITE_TWO:
            self.speed = 3
            self.strength = 1
            #self.points =
            #self.pattern = 
        elif sprite = ENEMY_SPRITE_THREE:
            self.speed = 1
            self.strength = 2
            #self.points =
            #self.pattern = 
        else:
            pass

        self.x = x
        self.y = y
        self.pat_step = pat_step
        
        self.image = load_image(sprite)
    
    def update(self):
        self.x = self.speed * self.pattern[pat_step][0]
        self.y = self.speed * self.pattern[pat_step][1]
        if self.x + self.rect.width < 0
            return false
            
        pat_step++
        if pat_step = len(pattern):
            pat_step = 0

            