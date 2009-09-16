
import pygame
from . import enemy_info
from . import util
from . import damageable

class AerialEnemy(pygame.sprite.Sprite, damageable.Damageable):

    def __init__(self, sprite, x, y, pat_step=0):
        pygame.sprite.Sprite.__init__(self)
        damageable.Damageable.__init__(self, AERIAL_ENEMY_HEALTH)
        if sprite == ENEMY_SPRITE_ONE:
            self.image = util.load_image(sprite)
            self.speed = 2
            self.strength = 1
            #self.points = 
            #self.pattern = ENEMY_PATTERN_STRAIGHT

        elif sprite == ENEMY_SPRITE_TWO:
            self.speed = 3
            self.strength = 1
            #self.points =
            #self.pattern =

        elif sprite == ENEMY_SPRITE_THREE:
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
        
        pat_step+=1
        if pat_step == len(pattern):
            pat_step = 0

        #return projectiles if shooting

            
