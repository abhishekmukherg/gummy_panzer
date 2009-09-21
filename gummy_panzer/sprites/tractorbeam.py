import pygame
import logging
import pkg_resources
import os
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects

EXTEND_SPEED = 5

class TractorBeam(pygame.sprite.Sprite):

    def __init__ (self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image("tractor_beam.png")

        self.rect.top = player.rect.bottom - 5
        self.rect.left = player.rect.center[0] - (self.rect.width / 2)

    def update (self, player):
        pass