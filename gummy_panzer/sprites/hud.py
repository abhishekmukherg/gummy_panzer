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
        self._draw_bar(self.player.sprite.energy, (383, 0), (0, 0, 255))
        hp = int(round(self.player.sprite.health * 100)
                / self.player.sprite.max_health)
        self._draw_bar(hp, (154, 0), (255, 0, 0))

    def _draw_bar(self, percent, location, color):
        percent = max(0, percent)
        percent = min(100, percent)
        rect = pygame.Rect(location, (218, 48))
        pygame.draw.rect(self.surface, color, rect,  1)
        rect.width = percent * 218 / 100
        pygame.draw.rect(self.surface, color, rect)

    def _draw_value(self, title, value, location, color):
        surf = self.font.render("%s: %d" % (title, value), True, color)
        self.surface.blit(surf, location)
