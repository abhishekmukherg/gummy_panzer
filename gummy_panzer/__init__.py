from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

import pygame, random
from gummy_panzer import settings
from gummy_panzer.sprites import player, hud, effects
from gummy_panzer.sprites import util, enemies, buildings, pedestrian


class EndOfGameException(Exception):
    pass


class Game(object):

    def __init__(self):
        pygame.init()
        LOG.info("Starting Game")
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,
                                    settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = pygame.sprite.GroupSingle(player.Player())
        self.player_bullets = pygame.sprite.Group()

        self.buildings_front = pygame.sprite.Group()
        self.buildings_back = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        self.hud = hud.Hud(100, 0, 0, 0)

        self.pedestrians = pygame.sprite.Group()

    def _generate_random_elements(self):
        if random.random() < settings.BUILDING_FREQ:
            LOG.debug("Generate Building - Generated")
            level = random.randint(0, 1)
            new_building = buildings.Building(level)
            group = self.buildings_front if level == 0 else self.buildings_back
            group.add(new_building)
        if random.random() < settings.ALIEN_FREQ:
            self.pedestrians.add(pedestrian.Alien())
        if random.random() < settings.HUMAN_FREQ:
            self.pedestrians.add(pedestrian.Human())

    def tick(self):
        LOG.debug("Game Tick")
        self._generate_random_elements()
        self.clock.tick(settings.FRAMES_PER_SECOND)
        pygame.display.update()
        for event in pygame.event.get():
            self._handle_event(event)
        bullets = self.player.sprite.update()
        map(self.player_bullets.add, bullets)
        self.player_bullets.update()
        self.pedestrians.update()
        self.buildings_front.update()
        self.buildings_back.update()
        self.hud.time = pygame.time.get_ticks()/1000
        self._draw()

    def _draw(self):
        self.__draw_background()
        for group in (self.buildings_back,
                self.player,
                self.player_bullets,
                self.buildings_front,
                self.pedestrians):
            self.__draw_spritegroup(group)
        self.hud.draw_hud(self.screen)

    def __draw_background(self):
        self.screen.fill((0, 0, 0))

    def __draw_spritegroup(self, group):
        for sprite in group:
            self.__draw_sprite(sprite)

    def __draw_sprite(self, sprite):
        if hasattr(sprite, "draw_area"):
            self.screen.blit(sprite.image,
                    sprite.rect.topleft,
                    sprite.draw_area)
        else:
            self.screen.blit(sprite.image, sprite.rect.topleft)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            raise EndOfGameException("Quit")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise EndOfGameException("Quit")
            # Reduce player's score by one for each attempt at firing
            elif event.key == pygame.K_SPACE:
                self.hud.score -= 1
        assert self.player.sprite is not None
        self.player.sprite.handle_event(event)

__all__ = ['main']
