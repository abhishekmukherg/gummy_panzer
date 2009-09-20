import pygame
import logging
from gummy_panzer.sprites import enemies, pedestrian
from gummy_panzer import settings

class Wave(pygame.sprite.Group):
    def __init__(self, distance, *args, **kwargs):
        pygame.sprite.Group.__init__(self, *args, **kwargs)
        self.distance = distance
        self.length = 0

    def update(self):
        if(self.distance >= 0):
            self.distance += settings.SCROLL_RATE
        else:
            for entry in self.contents:
                entry.update()
