import pygame
import logging
LOG = logging.getLogger(__name__)

class Hud(object):

    def __init__(self, health, energy, score, time):
        self.health = health
        self.energy = energy
        self.score = score
        self.time = time
        #self.rect_hp = pygame.Rect(10, 0, 150, 20)    #added test code
		#self.surf_hp = pygame.Surface((200, 200), flags=0, depth=0, masks=None)

    def draw_hud(self, surf):
        font = pygame.font.Font(None, 20)

        surfscore = font.render("Score:%d" % self.score, 1, (255, 0, 0))
        surf.blit(surfscore, (550, 0))

        surftime = font.render("Time:%d" % self.time, 1, (255, 0, 0))
        surf.blit(surftime, (400, 0))

        surfenergy = font.render("EN:%d" % self.energy, 1, (0, 255, 0))
        surf.blit(surfenergy, (200, 0))

        surfhealth = font.render("HP:%d" % self.health, 1, (0, 0, 255))
        surf.blit(surfhealth, (0, 0))
		
        #pygame.draw.rect(self.surf_hp, (0, 0, 255), self.rect_hp, width=1)    #added test code
        #surf.blit(self.surf_hp, (0, 0))