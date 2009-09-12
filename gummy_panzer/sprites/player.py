import pygame
from . import util

ACCEL = 2
MAX_V = 10

class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = util.load_image("player.png")
        self.rect = self.image.get_rect()
        class PhysicsProperty(object):
            x = 0
            y = 0
        self.v = PhysicsProperty()
        self.a = PhysicsProperty()

    def move_up(self):
        self.a.y = -ACCEL

    def move_down(self):
        self.a.y = ACCEL

    def stop_y(self):
        self.a.y = 0

    def stop_x(self):
        self.a.x = 0

    def move_right(self):
        self.a.x = ACCEL

    def move_left(self):
        self.a.x = -ACCEL

    def update(self):
        x, y = self.rect.topleft
        x += self.v.x
        y += self.v.y

        self.v.x = min(MAX_V, self.v.x + self.a.x)
        self.v.x = max(-MAX_V, self.v.x)
        self.v.y = min(MAX_V, self.v.y + self.a.y)
        self.v.y = max(-MAX_V, self.v.y)

        self.a.x, self.a.y = 0, 0

        self.rect.topleft = x, y
