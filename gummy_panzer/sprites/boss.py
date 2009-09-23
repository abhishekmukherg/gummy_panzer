import logging
import pygame
import random

import gummy_panzer
from gummy_panzer import settings
from gummy_panzer.sprites import damageable
from gummy_panzer.sprites import effects
from gummy_panzer.sprites import weapons
from gummy_panzer.sprites import util
from gummy_panzer import settings


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

    STATE_PROB = {State.CHILLIN: .8,
                  State.ATTACKING: .1,
                  State.CREATING_BERNARD: .1,
                  State.CREATING_FRED: .1,
                  State.CREATING_GERTRUDE: .1,
                  }

    points = 1000

    def __init__(self, loc, player, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        damageable.Damageable.__init__(self, BOSS_HEALTH)
        self.image = pygame.Surface((200, 200))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()
        self.rect.topright = loc
        self.state = Boss.State.CHILLIN
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.player = player
        self.__state_tick = 0
        self.__moving_tick = 0
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

    def dying(self):
        screen = pygame.display.set_mode(
                (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        image = util.load_image("victoryscreen.png")
        clock = pygame.time.Clock()
        screen.blit(image, (10, 10))
        pygame.display.update()
        while True:
            clock.tick(settings.FRAMES_PER_SECOND)
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    raise gummy_panzer.EndOfGameException("Quit")
                    

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
            decision_horiz = random.randint(0,3)
            decision_vert = random.randint(0,3)
            if self.__moving_tick == 0:
                if decision_horiz == 0:
                    self.moving_right = True
                    self.moving_left = False
                elif decision_horiz == 1:
                    self.moving_right = False
                    self.moving_left = True
                else:
                    self.moving_right = self.moving_left = False

                if decision_vert == 0:
                    self.moving_up = True
                    self.moving_down = False
                elif decision_vert == 1:
                    self.moving_up = False
                    self.moving_down = True
                else:
                    self.moving_up = self.moving_down = False

            self.__moving_tick += 1
            
            if self.__moving_tick == 5:
                self.__moving_tick =0

            if self.moving_left:
                self.rect.x -= random.randint(4,15)
            elif self.moving_right:
                self.rect.x += random.randint(4,15)

            if self.moving_up:
                self.rect.y -= random.randint(4,15)
            elif self.moving_down:
                self.rect.y += random.randint(4,15)

            if self.rect.x > settings.SCREEN_WIDTH - self.rect.width:
                self.rect.x = settings.SCREEN_WIDTH - self.rect.width
            elif self.rect.x < self.player.sprite.rect.width * 2:
                self.rect.x = self.player.sprite.rect.width * 2

            if self.rect.y > settings.SCREEN_HEIGHT - self.rect.height:
                self.rect.y = settings.SCREEN_HEIGHT - self.rect.height
            elif self.rect.y < 0:
                self.rect.y = 0

        elif self.state == Boss.State.ATTACKING:
            LOG.info("Attacking")
        elif self.state == Boss.State.CREATING_BERNARD:
            LOG.info("Creating Bernard")
        elif self.state == Boss.State.CREATING_FRED:
            LOG.info("Creating Fred")
        elif self.state == Boss.State.CREATING_GERTRUDE:
            LOG.info("Creating Gertrude")
        return {"enemies": [], "bullets": []}

    

        
