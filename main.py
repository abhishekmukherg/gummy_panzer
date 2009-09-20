import pygame
import gummy_panzer, sys
g = gummy_panzer.Game()

try:
    while True:
        g.tick()
except gummy_panzer.EndOfGameException:
    pygame.quit()
