import pygame
import logging
from gummy_panzer.sprites import enemies, pedestrian
from gummy_panzer import settings

class Wave(pygame.sprite.Group):
    def __init__(self, distance):
        self.distance = distance
        self.contents = []

    def update(self):
        if(self.distance >= settings.SCREEN_WIDTH):
            self.distance += settings.SCROLL_RATE
        else:
            for entry in self.contents
                entry.update()
