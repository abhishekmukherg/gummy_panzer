
import pygame
from . import enemy_info, damageable, util

class AerialEnemy(pygame.sprite.Sprite, damageable.Damageable):

    def __init__(self, sprite, x, y, pat_step=0):
        pygame.sprite.Sprite.__init__(self)
        damageable.Damageable.__init__(self, enemy_info.AERIAL_ENEMY_HEALTH)
        if sprite == enemy_info.SPRITE_ONE:
            self.speed = 2
            self.strength = 1
            #self.points = 
            self.pattern = enemy_info.ENEMY_PATTERN_STRAIGHT

        elif sprite == enemy_info.SPRITE_TWO:
            self.speed = 3
            self.strength = 1
            #self.points =
            self.pattern = enemy_info.PATTERN_WAVE_MID_UP

        elif sprite == enemy_info.SPRITE_THREE:
            self.speed = 1
            self.strength = 2
            #self.points =
            self.pattern = enemy_info.PATTERN_DIAG_UP
        else:
            self.speed = 1
            self.strength = 1
            self.pattern = enemy_info.PATTERN_DIAG_DOWN

        self.x = x
        self.y = y
        self.image = util.load_image(sprite)
        self.rect = self.image.get_rect()
        self.state = enemy_info.STATE_MOVING
        self.anim_frame = 0
        self.draw_area = pygame.Rect(self.anim_frame * enemy_info.STATE_W,
                                     self.state * enemy_info.STATE_H,
                                     enemy_info.STATE_W, enemy_info.STATE_H)
        self.pat_step = pat_step
        self.anim_update_counter = 0
        
        self.image = util.load_image(sprite)
    
    def update(self):
        self.rect.x = self.pattern[self.pat_step][0]
        self.rect.y = self.pattern[self.pat_step][1]

        #if self.anim_update_counter == self.speed:
        #    self.anim_frame+=1
        #if self.anim_frame >= enemy_info.ANIM_LEN[self.state]:
        #    self.anim_frame = 0

        self.draw_area = pygame.Rect(self.anim_frame * enemy_info.STATE_W,
                                     self.state * enemy_info.STATE_H,
                                     enemy_info.STATE_W, enemy_info.STATE_H)

        self.pat_step+=1
        if self.pat_step == len(self.pattern):
            self.pat_step = 0

        # self.anim_update_counter+=1

        #return projectiles if shooting

            
