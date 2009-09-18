
import pygame
import logging
import random
from . import enemy_info, damageable, util, effects

LOG = logging.getLogger(__name__)

class AerialEnemy(effects.SpriteSheet, damageable.Damageable):

    def __init__(self, sprite, loc, pat_step=0):
        damageable.Damageable.__init__(self, enemy_info.AERIAL_ENEMY_HEALTH)
        effects.SpriteSheet.__init__(self, util.load_image(sprite),
                (enemy_info.STATE_W, enemy_info.STATE_H))
        if sprite == enemy_info.SPRITE_ONE:
            self.speed = 15
            self.strength = 1
            #self.points = 
            self.pattern = enemy_info.PATTERN_STRAIGHT

        elif sprite == enemy_info.SPRITE_TWO:
            self.speed = 20
            self.strength = 1
            #self.points =
            self.pattern = enemy_info.PATTERN_WAVE_MID_UP

        elif sprite == enemy_info.SPRITE_THREE:
            self.speed = 10
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
        LOG.info(repr(self.speed))
        self.rect.left += ( self.speed * self.pattern[self.pat_step][0] )
        self.rect.top += ( self.speed * self.pattern[self.pat_step][1] )

        if self.anim_update_counter == self.speed:
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

            
