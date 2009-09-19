#notes on Background Carnage:
#Must code for building damage and collapsing
#code for little animations in the background?  Or am I just coding buildings here?

#notes on sound-
#Enemy A:  Move Sound, Attack Sound, Fall Sound, Die Sound
#Enemy B:  Move Sound, Attack Sound, Fall Sound, Die Sound
#Enemy C:  Move Sound, Attack Sound, Fall Sound, Die Sound

#Boss:  Move Sound, Attack Sound A, B, C, Fall Sound, Die Sound

import pygame
from .. import settings
from . import effects, util
#+= settings.SCROLL_RATE

#Building:  Damage Sound, Fall Sound, Die Sound
#Player:  Move Sound, Attack Sound A, B C, Fall Sound, Die Sound
class Building(effects.SpriteSheet):
    def __init__(self, lev):
        #Fallspeed is the number of pixels the building falls each incriment when it is being destroyed
        #Image is the location of the building spritesheet.  Carnageimage is the dust when the building collapses
        #Height should be 0 for below the street, 2 for above the street, 1 for on the street (1 should not be used)
        #state is 0 for whole, 1 for damaged, 2 for destroyed.
        effects.SpriteSheet.__init__(self, util.load_image("building.png"),
                (50, 100))
        #self.wavex=0    #X position in the wave
        self.height=100   #Height in pixels of building
        self.level=lev  #Level 0 for below street, 1 for above street
        self.fallspeed=1#How many pixels it falls each loop.
        
        if self.level==0:      
            self.rect.topleft=(600, 400)
        elif self.level==1:
            self.rect.topleft=(600, 200)


        self.state=0    #State of the building.  0 intact, 1 damaged, 2 destroyed.
        
        
   # def draw(self, surface):
        #note that when state changes it will make the building sprite change(in this case move over 50 pixels)
    #    if self.alive ==2:
     #       screen.blit(self.image, self.rect, pygame.Rect(50*(self.state), 0, 50, 50))  # change this
        #loop over all enemies,  checking fallers against ground height.  Set enemy to explode, add effects, and all buildings, check if it's in the blast radius.

    def update(self):
        self.rect.left+= settings.SCROLL_RATE

        #    self.state+=1
         #   if self.state ==2:
        #        self.alive=2
        #if self.alive==2:
         #   self.rect.move_ip(0,fallspeed)
         #   height-=1
         #               if height==0:
          #                  self.alive=0
                
            
            
        #INTACT STATE: 0
        #DAMAGED STATE: 1
        #DESTROYED STATE: 2
        #If state is intact display sprite is 1
        #If state is damaged display sprite is 2
        #If state is Destroyed display sprite is 3
        #If building takes 1 damage, change sprite