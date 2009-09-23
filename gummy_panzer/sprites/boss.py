import logging
import pygame
import random

from gummy_panzer.sprites import damageable
from gummy_panzer.sprites import effects
from gummy_panzer.sprites import weapons


LOG = logging.getLogger(__name__)


BOSS_HEALTH = 100


class Boss(pygame.sprite.Sprite, damageable.Damageable):

    class State:
        CHILLIN = 0
        ATTACKING = 1
        CREATING_BERNARD = 2
        CREATING_FRED = 3
        CREATING_GERTRUDE = 4

    STATE_TICKS = {State.CHILLIN: 10,
                   State.ATTACKING: 35,
                   State.CREATING_BERNARD: 10,
                   State.CREATING_FRED: 10,
                   State.CREATING_GERTRUDE: 10,
                   }

    STATE_PROB = {State.CHILLIN: .7,
                  State.ATTACKING: .5,
                  State.CREATING_BERNARD: .1,
                  State.CREATING_FRED: .1,
                  State.CREATING_GERTRUDE: .1,
                  }

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
        class Physics:
            x = 0
            y = 0
        self.velocity = Physics()
        self.acceleration = Physics()

    def _random_state(self):
        max_rand = sum(Boss.STATE_PROB.itervalues())
        rand = random.random() * max_rand
        for key, value in Boss.STATE_PROB.iteritems():
            rand -= value
            if rand < 0:
                return key
        assert False

    def _change_to_random_state(self):
        self.state = self._random_state()
        if self.state == Boss.State.ATTACKING:
            laser = weapons.Laser()
            laser.rect.right = self.rect.left
            laser.rect.centery = self.rect.centery
            return {"bullets": [laser]}
        return {}

    def update(self):
        if self.__state_tick >= Boss.STATE_TICKS[self.state]:
            retdict = {}
            if self.state == Boss.State.CHILLIN:
                retdict.update(self._change_to_random_state())
            else:
                self.state = Boss.State.CHILLIN
            self.__state_tick = 0
            if "enemies" not in retdict:
                retdict["enemies"] = []
            if "bullets" not in retdict:
                retdict["bullets"] = []
            return retdict
        self.__state_tick += 1
        if self.state == Boss.State.CHILLIN:
            LOG.info("Chillin")

        elif self.state == Boss.State.ATTACKING:
            LOG.info("Attacking")
        elif self.state == Boss.State.CREATING_BERNARD:
            LOG.info("Creating Bernard")
        elif self.state == Boss.State.CREATING_FRED:
            LOG.info("Creating Fred")
        elif self.state == Boss.State.CREATING_GERTRUDE:
            LOG.info("Creating Gertrude")
        return {"enemies": [], "bullets": []}

    

        
