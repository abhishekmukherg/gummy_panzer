import pygame
import random
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects


class Pedestrian(effects.SpriteSheet):

    def __init__(self, depth, animate):
        """Creates a pedestrian

        self.splattered is whether the class has been killed or not

        """
        effects.SpriteSheet.__init__(self,
                util.load_image("bad_alien_running.png"), (32, 32))
        self.animation = animate
        self.splattered = False
        self.depth = depth


    def beam_me_up(self):
        self.rect.y -=4
        if player.rect.y == self.rect.y:
            self.kill()
        if self.animation == _AnimationStates.BEAMING_UP:
            return False
        else:
            self.animation = _AnimationStates.BEAMING_UP
            return True

    def splat_me(self):
        """return a value for (splatterm a modification for depth so that blood
        always appears below non-splattered)
        
        """
        if self.splattered:
            return
        elif self.animation == 3:
            return
        else:
            self.splattered = True
            return (1, self.depth + 20)

    def update(self):
        """function to change the horizontal location of pedestrians"""
        if self.splattered:
            self.rect.x -= 2
        if self.animation == 0:
            self.rect.x -= 3
        if self.animation == 1:
            self.rect.x -= 1
        
        if pygame.time.get_ticks() % 4 == 0:
            self.anim_frame = (self.anim_frame + 1) % 6


class Alien(Pedestrian):

    def __init__(self, animate):
        Pedestrian.__init__(self, 10, animate)
        effects.SpriteSheet.__init__(self,
                util.load_image("bad_alien_running.png"), (32, 32))


class Human(Pedestrian):

    def __init__(self, animate):
        Pedestrian.__init__(self, 20, animate)
        if self.animation == 0:
            effects.SpriteSheet.__init__(self,
                    util.load_image("dinoleftsprite.png"), (36, 32))
        elif self.animation == 1:
            effects.SpriteSheet.__init__(self,
                util.load_image("dinospritefinal.png"), (36, 32))
            


