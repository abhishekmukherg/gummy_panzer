import pygame
import logging

LOG = logging.getLogger(__name__)

class SpriteSheet(pygame.sprite.Sprite):

    def __init__(self, image, image_width, *groups):
        """Makes a simple sprite sheet holder
        
        image: A Surface class
        image_size: (WxH) of an individual sprite
        
        """
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.rect = image.get_rect()
        self.draw_area = None
        self.draw_area = pygame.Rect((0, 0),
                (image_width, image.get_height()))
        self.anim_frame = 0
        assert self.draw_area

    @property
    def anim_frame(self):
        """Animation frame of the sprite sheet"""
        return self.__anim_frame

    @anim_frame.setter
    def anim_frame(self, val):
        self.__anim_frame = val
        self.draw_area.left = val * self.draw_area.width
        LOG.debug("Draw area rect=%s" % unicode(self.draw_area))
