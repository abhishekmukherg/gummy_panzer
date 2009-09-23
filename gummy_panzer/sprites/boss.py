import logging
import pygame

from gummy_panzer.sprites import damageable
from gummy_panzer.sprites import effects
from gummy_panzer.sprites import weapons


LOG = logging.getLogger(__name__)


BOSS_HEALTH = 100


class Boss(pygame.sprite.Sprite, damageable.Damageable):

    class State:
        CHILLIN = 0
        ATTACKING = 1
        CREATING_GROUND = 2
        CREATING_AIR = 3

    STATE_TICKS = {State.CHILLIN: 10,
                   State.ATTACKING: 10,
                   State.CREATING_GROUND: 10,
                   State.CREATING_AIR: 10}

    points = 1000

    def __init__(self, loc, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        damageable.Damageable.__init__(self, BOSS_HEALTH)
        self.image = pygame.Surface((200, 200))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()
        self.rect.topright = loc
        self.state = Boss.State.CHILLIN
        self.__state_tick = 0

    def update(self):
        if self.__state_tick >= Boss.STATE_TICKS[self.state]:
            self.state = Boss.State.CHILLIN
            self.__state_tick = 0
            return
        self.__state_tick += 1
        if self.state == Boss.State.CHILLIN:
            LOG.info("Chillin")

    

        
