import pygame
from gummy_panzer.sprites import damageable
from gummy_panzer.sprites import effects
from gummy_panzer.sprites import weapons


BOSS_HEALTH = 100


class Boss(pygame.sprite.Sprite, damageable.Damageable):

    points = 1000

    def __init__(self, loc, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        damageable.Damageable.__init__(self, BOSS_HEALTH)
        self.image = pygame.Surface((200, 200))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()

        
