import pygame
import logging
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects

#TODO: blit it, handle picking people up, draw circle when touching ground

LOG = logging.getLogger(__name__)

EXTEND_SPEED = 10

class TractorBeam(pygame.sprite.Sprite):

    def __init__ (self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image("tractor_beam.png")

        self.rect = self.image.get_rect()
        self.rect.top = player.rect.bottom - 5
        self.rect.left = player.rect.center[0] - (self.rect.width / 2)

        self.extending = False
        self.extended = False
        self.retracting = False
        self.abducting = False
        self.draw_area = pygame.Rect(self.rect.topleft,(self.rect.width, 0))

    @property
    def touching_ground(self):
        return ((self.draw_area.y + self.draw_area.height) >
                    (settings.SCREEN_HEIGHT * .95))

    def update (self, player):
        if self.extending:
            if self.touching_ground:
                LOG.info("loc: (%d,%d), height: %d, done extending" %
                                (self.draw_area.x, self.draw_area.y,
                                self.draw_area.height))
                self.extending = False
                self.extended = True
                self.draw_area.height = ((settings.SCREEN_HEIGHT * .95) -
                                                            self.draw_area.y)
                #draw circle @bottom
            else:
                LOG.info("loc: (%d,%d), height: %d, extending" %
                                (self.draw_area.x, self.draw_area.y,
                                self.draw_area.height))
                self.draw_area.height += EXTEND_SPEED

        elif self.abducting:
            pass

        elif self.retracting:
            if self.draw_area.height <= 0:
                LOG.info("loc: (%d,%d), height: %d, done retracting" %
                                (self.draw_area.x, self.draw_area.y,
                                self.draw_area.height))
                self.draw_area.height = 0
                self.retracting = False
            else:
                LOG.info("loc: (%d,%d), height: %d, retracting" %
                                (self.draw_area.x, self.draw_area.y,
                                self.draw_area.height))
                self.draw_area.height -= EXTEND_SPEED

        elif self.extended:
            LOG.info("loc: (%d,%d), height: %d, fully extended!" %
                                (self.draw_area.x, self.draw_area.y,
                                self.draw_area.height))
            self.draw_area.height = ((settings.SCREEN_HEIGHT * .95) -
                                (self.draw_area.y + self.draw_area.height))
        
        self.rect.top = player.rect.bottom - 5
        self.rect.left = player.rect.center[0] - (self.rect.width / 2)
