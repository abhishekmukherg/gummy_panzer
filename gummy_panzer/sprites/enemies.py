import pygame
import logging
import random
from gummy_panzer.sprites import enemy_info, damageable, util, effects
from gummy_panzer import settings

LOG = logging.getLogger(__name__)

class AerialEnemy(effects.SpriteSheet, damageable.Damageable):

    def __init__(self, sprite, loc, speed=(None, None), pattern = None,
                                                              pat_step=0):
        damageable.Damageable.__init__(self, enemy_info.AERIAL_ENEMY_HEALTH)
        effects.SpriteSheet.__init__(self, util.load_image(sprite),
                (enemy_info.STATE_W, enemy_info.STATE_H))
        self.points = 10
        if sprite == enemy_info.SPRITE_ONE:
            if speed[0] == None:
                self.speedx = 6
            else:
                self.speedx = speed[0]
            if speed[1] == None:
                self.speedy = 6
            else:
                self.speedy = speed[1]
            self.strength = 1
            #self.points = 
            if pattern == None:
                self.pattern = enemy_info.PATTERN_STRAIGHT
            else:
                self.pattern = pattern

        elif sprite == enemy_info.SPRITE_TWO:
            if speed[0] == None:
                self.speedx = 4
            else:
                self.speedx = speed[0]
            if speed[1] == None:
                self.speedy = 5
            else:
                self.speedy = speed[1]
            self.strength = 1
            #self.points =
            if pattern == None:
                self.pattern = enemy_info.PATTERN_WAVE_MID_UP
            else:
                self.pattern = pattern

        elif sprite == enemy_info.SPRITE_THREE:
            if speed[0] == None:
                self.speedx = 10
            else:
                self.speedx = speed[0]
            if speed[1] == None:
                self.speedy = 10
            else:
                self.speedy = speed[1]
            self.strength = 2
            #self.points =
            self.pattern = enemy_info.PATTERN_DIAG_UP
        else:
            self.speed = 1000
            self.strength = 1
            self.pattern = enemy_info.PATTERN_DIAG_DOWN

        LOG.debug("spam " + unicode(self.rect))
        self.rect.topleft = loc
        LOG.debug("eggs " + unicode(self.rect))

        self.state = enemy_info.STATE_MOVING
        self.pat_step = pat_step
        self.anim_update_counter = 0
    
    def update(self):
        self.rect.left += ( self.speedx * self.pattern[self.pat_step][0] +
                                                        settings.SCROLL_RATE)
        self.rect.top += ( self.speedy * self.pattern[self.pat_step][1] )

        if self.anim_update_counter == 5:
            self.anim_frame += 1
            self.anim_update_counter = 0
        if self.anim_frame >= enemy_info.ANIM_LEN[self.state]:
            self.anim_frame = 0

        self.state = random.randint(0, 2)

        self.pat_step+=1
        if self.pat_step == len(self.pattern):
            self.pat_step = 0

        self.anim_update_counter+=1
        LOG.debug("eggs " + unicode(self.rect))

        #return projectiles if shooting

            
