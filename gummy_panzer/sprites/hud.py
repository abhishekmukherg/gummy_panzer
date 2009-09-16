import pygame

class Hud(object):

    def __init__(self, health, energy, score, time):
        self.health = health
        self.energy = energy
        self.score = score
        self.time = time        

    def draw_hud(self, surf):
        font = pygame.font.Font(None, 20)

        surfscore = font.render("Score:%d" % self.score, 1, (255, 0, 0))
        surf.blit(surfscore, (600, 0))

        surftime = font.render("Time:%d" % self.time, 1, (255, 0, 0))
        surf.blit(surftime, (400, 0))

        surfenergy = font.render("EN:%d" % self.energy, 1, (0, 255, 0))
        surf.blit(surfenergy, (200, 0))

        surfhealth = font.render("HP:%d" % self.health, 1, (0, 0, 255))
        surf.blit(surfhealth, (0, 0))
