from __future__ import division

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

    def draw_hud(self, surf):
        self._draw_value("Score", self.score, (550, 0), (255, 0, 0))
        self._draw_value("Time", self.time, (400, 0), (255, 0, 0))
        self._draw_bar("EN", self.player.sprite.energy, (200, 0), (0, 0, 255))
        hp = int(round(self.player.sprite.health * 100)
                / self.player.sprite.max_health)
        self._draw_bar("HP", hp, (0, 0), (255, 0, 0))

    def _draw_bar(self, title, percent, location, color):
        percent = max(0, percent)
        percent = min(100, percent)
        surf = self.font.render("%s: " % title, True, color)
        self.surface.blit(surf, location)
        location = (location[0] + surf.get_rect().width, location[1])
        rect = pygame.Rect(location, (100, 15))
        pygame.draw.rect(self.surface, color, rect,  1)
        rect.width = percent
        pygame.draw.rect(self.surface, color, rect)

    def _draw_value(self, title, value, location, color):
        surf = self.font.render("%s: %d" % (title, value), True, color)
        self.surface.blit(surf, location)
