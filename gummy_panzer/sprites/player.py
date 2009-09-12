import pygame
from . import util

class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = util.load_image("player.png")
        self.rect = self.image.get_rect()
