from __future__ import division
from gummy_panzer.sprites import util

import pygame
import logging
import pygame
import weakref
LOG = logging.getLogger(__name__)


class Hud(object):

    def __init__(self, player, surface):
        self.player = pygame.sprite.GroupSingle(player)
        self.surface = surface
        self.score = 0
        self.time = 0
        self.font = pygame.font.Font(None, 20)
        self.health_fill = util.load_image("healthfill.png")
        self.energy_fill = util.load_image("energyfill.png")

    def draw_hud(self, surf):
        self._draw_bar(self.player.sprite.energy, (383, 8), (0, 0, 255), self.energy_fill)
        hp = int(round(self.player.sprite.health * 100)
                / self.player.sprite.max_health)
        self._draw_bar(hp, (154, 8), (255, 0, 0), self.health_fill)

    def _draw_bar(self, percent, location, color, bar_image):    
        percent = max(0, percent)
        percent = min(100, percent)
        rect = pygame.Rect((0, 0), (percent * 218 / 100, 48))
        self.surface.blit(bar_image, location, rect)

    def _draw_value(self, title, value, location, color):
        surf = self.font.render("%s: %d" % (title, value), True, color)
        self.surface.blit(surf, location)
