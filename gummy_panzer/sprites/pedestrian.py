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
                util.load_image("insectsprite.png"), (32, 32))
        self.animation = animate
        self.splattered = False
        self.depth = depth
        self.drawc = 0
        self.drawcount = 4
        self.beaming = 0
        self.speed = random.uniform(0.1, 1.9)


    def beam_me_up(self):
        self.beaming = 1

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
        if self.beaming == 1:
            self.rect.y -=15
        elif self.splattered:
            self.rect.x -= 2
        elif self.animation == 0:
            self.rect.x -= 3
        elif self.animation == 1:
            self.rect.x -= 1  
        elif self.animation == 2:
            self.rect.x -=2
        
        self.drawc+=1
        if isinstance(self, Human):
            if self.drawc == self.drawcount:
                self.anim_frame = (self.anim_frame + 1) % 6
                self.drawc = 0
        elif isinstance(self, Alien):
            if self.drawc == self.drawcount:
                self.anim_frame = (self.anim_frame + 1) % 4
                self.drawc = 0 
        else:
            if self.drawc == self.drawcount:
                self.anim_frame = (self.anim_frame + 1) % 1
                self.drawc = 0


class Alien(Pedestrian):

    def __init__(self, animate):
        Pedestrian.__init__(self, 10, animate)
        if self.animation == 0:
            effects.SpriteSheet.__init__(self,
                    util.load_image("insectsprite.png"), (36, 32))
        elif self.animation == 1:
            effects.SpriteSheet.__init__(self,
                util.load_image("insectspriteright.png"), (36, 32))

class Human(Pedestrian):

    def __init__(self, animate):
        Pedestrian.__init__(self, 20, animate)
        if self.animation == 0:
            effects.SpriteSheet.__init__(self,
                    util.load_image("dinoleftsprite.png"), (36, 32))
        elif self.animation == 1:
            effects.SpriteSheet.__init__(self,
                util.load_image("dinospritefinal.png"), (36, 32))
            
class Health(Pedestrian):

    def __init__(self, animate):
        Pedestrian.__init__(self, 20, animate)
        effects.SpriteSheet.__init__(self,
                    util.load_image("health_pack.png"), (36, 32))
       

