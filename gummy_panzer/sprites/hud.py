import pygame
from . import util
from .. import settings

class hud(object):

    def __init__(self, health, energy, score, time):
        self.health = health
        self.energy = energy
        self.score = score
        self.time = time        

    def draw_hud(self, surf):
        f = pygame.font.Font(None, 20)
        surfscore = f.render("Score:%d"%self.score, 1, (0,0,0))
        surf.blit(surfscore, 600, 0)
        surftime = f.render("Time:%d"%self.time, 1, (0,0,0)
        surf.blit(surftime, 400, 0)
        surfenergy = f.render("EN:%d"%self.energy, 1, (0, 255, 0)
        surf.blit(surfenergy, 200, 0)
        surfhealth = f.render("HP:%d"%self.health, 1, (0, 0, 255)
        surf.blit(surfhealth, 0, 0)
