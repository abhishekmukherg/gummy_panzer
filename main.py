import pygame
import gummy_panzer
import pkg_resources
import os
#new imports for this tutorial intro
from gummy_panzer import util, settings
from pygame.locals import *

settings.SCREEN_WIDTH = 800
settings.SCREEN_HEIGHT = 600
INTROWIDTH = 1600
NUMINTROS = 4
INTRO = 0
MAINMENU = 1
PLAYMODE = 2


pygame.display.set_caption("GummyPanzer")
screen = pygame.display.set_mode((800, 600))

state = INTRO
introc = 0
intronum = 0
introsurf_cache = {0: util.load_image("intro0.png").convert(),
        1: util.load_image("intro1.png").convert(),
        2: util.load_image("intro2.png").convert(),
        3: util.load_image("intro3.png").convert(),
        }
introcount = 800

    #font for the control box
    
pygame.mixer.music.load(pkg_resources.resource_stream("gummy_panzer",
    os.path.join("Sounds", "menu.ogg")))
pygame.mixer.music.play(-1)
while 1 and state == INTRO:

    if introc == introcount:
        introc = 0
        intronum += 1
        if intronum == NUMINTROS:
            state = MAINMENU
            continue
    else:
        introc += 1

    if intronum in introsurf_cache:
        introsurf = introsurf_cache[intronum]

    screen.blit(introsurf, (0, 0), (introc, 0, 800, 600))
        #KEYPRESS EVENTS__+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+=-+_+_+_
    for e in pygame.event.get():

            #QUIT is the big red X button on the window bar
        if e.type == QUIT:
            pygame.quit()
            

            #Check if a key was pressed
        if e.type == KEYDOWN:

                #Quit if the Escape key is pressed
            if e.key == K_ESCAPE:
                state = MAINMENU
                
            else:
                introc = introcount



        #_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+___+




    pygame.display.flip()

while 1 and state == MAINMENU:
    mainmenusurf = util.load_image("startmenu.bmp").convert()

    for e in pygame.event.get():

            #QUIT is the big red X button on the window bar
        if e.type == QUIT:
            pygame.quit()
            

            #Check if a key was pressed
        if e.type == KEYDOWN:

                #Quit if the Escape key is pressed
            if e.key == K_ESCAPE:
                pygame.quit()
                
            else:
                pygame.mixer.music.load(pkg_resources.resource_stream("gummy_panzer",
                    os.path.join("Sounds", "background.ogg")))
                pygame.mixer.music.play(-1)
                state = PLAYMODE
        #_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+


    screen.blit(mainmenusurf, (0, 0))
    pygame.display.flip()


g = gummy_panzer.Game()
try:
    while True:
        g.tick()
except gummy_panzer.EndOfGameException:
    pygame.quit()
