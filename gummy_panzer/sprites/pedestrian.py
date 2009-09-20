import pygame
import random
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects


class _AnimationStates(object):
    STANDING = 0
    RUNNING_LEFT = 1
    RUNNING_RIGHT = 2
    BEAMING_UP = 3


class Pedestrian(effects.SpriteSheet):

    def __init__(self, depth):
        """Creates a pedestrian

        self.animation is the AnimationState the class is in.
        self.splattered is whether the class has been killed or not

        """
        effects.SpriteSheet.__init__(self,
                util.load_image("bad_alien_running.png"), (32, 32))
        self.animation = _AnimationStates.STANDING
        self.splattered = False
        self.depth = depth

    @property
    def animation(self):
        return self.__animation

    @animation.setter
    def animation(self, val):
        self.__animation = val

        states = {_AnimationStates.STANDING: 0,
                _AnimationStates.RUNNING_LEFT: 1,
                _AnimationStates.RUNNING_RIGHT: 2,
                _AnimationStates.BEAMING_UP: 3,
                }

        self.anim_frame = states[self.animation]


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
        if self.animation == _AnimationStates.RUNNING_LEFT:
            self.rect.x -= 3
        if self.animation == _AnimationStates.RUNNING_RIGHT:
            self.rect.x -= 1
        if self.animation == _AnimationStates.STANDING:
            self.rect.x -= 2


class Alien(Pedestrian):

    def __init__(self):
        Pedestrian.__init__(self, 10)
        effects.SpriteSheet.__init__(self,
                util.load_image("bad_alien_running.png"), (32, 32))


class Human(Pedestrian):

    def __init__(self):
        Pedestrian.__init__(self, 20)				
        effects.SpriteSheet.__init__(self,
                util.load_image("bad_sprite_running.png"), (32, 32))


