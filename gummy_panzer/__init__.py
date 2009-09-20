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
        if random.random() < settings.FRONT_BUILDING_FREQ:
            LOG.debug("Generate Building - Generated front")
            self.buildings_front.add(buildings.Building(0))
        if random.random() < settings.BACK_BUILDING_FREQ:
            LOG.debug("Generate Building - Generated back")
            self.buildings_back.add(buildings.Building(1))
        if random.random() < settings.ALIEN_FREQ:
            random_height = random.randint(1, 40)
            new_pedestrian = pedestrian.Alien()
            new_pedestrian.rect.bottomleft = (settings.SCREEN_WIDTH,
                    settings.SCREEN_HEIGHT - random_height)
            self.pedestrians.add(new_pedestrian)
        if random.random() < settings.HUMAN_FREQ:
            random_height = random.randint(1, 40)
            new_pedestrian = pedestrian.Human()
            new_pedestrian.rect.bottomleft = (settings.SCREEN_WIDTH,
                    settings.SCREEN_HEIGHT - random_height)
            self.pedestrians.add(new_pedestrian)

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
