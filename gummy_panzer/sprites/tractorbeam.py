import pygame
import logging
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects

#TODO: blit it, handle picking people up, draw circle when touching ground

LOG = logging.getLogger(__name__)

EXTEND_SPEED = 10

class TractorBeam(effects.SpriteSheet):

    def __init__ (self, player, *groups):
        #pygame.sprite.Sprite.__init__(self)
        #self.image = util.load_image("tractor_beam_green.png")
        sheet = util.load_image("tractor_beam_anim.png")
        image_size = (70, 100)
        effects.SpriteSheet.__init__(self, sheet, image_size, *groups)
        self.rect.width = 70
        self.rect.height = 599
        self.rect.top = player.rect.bottom -100
        self.rect.left = player.rect.center[0] - (self.rect.width / 2)

        self.extending = False
        self.extended = False
        self.retracting = False
        self.abducting = False
        #self.draw_area = pygame.Rect(self.rect.topleft,(self.rect.width, 0))
        self.draw_area = pygame.Rect((0,self.rect.height),(self.rect.width, 0))
        self.drawc = 0
        self.drawcount = 2
    @property
    def touching_ground(self):
        return ((self.rect.y + self.draw_area.height) >
                    (settings.SCREEN_HEIGHT * .98))

    def update (self, player):
        self.drawc+=1

        if self.drawc == self.drawcount:
            self.anim_frame = (self.anim_frame + 1) % 19
            self.drawc = 0
        if self.extending:
            LOG.info("loc: (%d,%d), height: %d, extending" %
                            (self.rect.x, self.rect.y,
                            self.draw_area.height))
            self.draw_area.height += EXTEND_SPEED
            self.draw_area.y -=EXTEND_SPEED
            if self.touching_ground:
                LOG.info("loc: (%d,%d), height: %d, done extending" %
                                (self.rect.x, self.rect.y,
                                self.draw_area.height))
                self.extending = False
                self.extended = True
                self.draw_area.height = ((settings.SCREEN_HEIGHT * .98) -
                                                            self.rect.y)
                #draw circle @bottom

        elif self.abducting:
            pass

        elif self.retracting:
            LOG.info("loc: (%d,%d), height: %d, retracting" %
                            (self.rect.x, self.rect.y,
                            self.draw_area.height))
            self.draw_area.height -= EXTEND_SPEED
            self.draw_area.y +=EXTEND_SPEED
            if self.draw_area.height <= 0:
                LOG.info("loc: (%d,%d), height: %d, done retracting" %
                                (self.rect.x, self.rect.y,
                                self.draw_area.height))
                self.draw_area.height = 0
                self.draw_area.y = self.rect.height
                self.retracting = False

        elif self.extended:
            LOG.info("loc: (%d,%d), height: %d, fully extended!" %
                                (self.rect.x, self.rect.y,
                                self.draw_area.height))
            self.draw_area.height = ((settings.SCREEN_HEIGHT * .98) -
                                (self.rect.top))
            self.draw_area.y = self.rect.height - self.draw_area.height
        
        self.rect.top = player.rect.bottom - 30
        self.rect.left = player.rect.center[0] - (self.rect.width / 2)
