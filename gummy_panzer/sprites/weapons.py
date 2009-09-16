import pygame
from . import util


MACHINE_GUN_V = 20


class WeaponFactory(object):
    
    """
    Base class for a generic weapon with a cooldown timer
    """
    
    def __init__(self, cooldown_ticks, weapon_class):
        """Creates a weapon for a ship

        cooldown_ticks is the number of ticks for it to cooldown
        weapon_class should be a class that has a no-args constructor for the
          weapon itself

        """
        self.cooldown_ticks = cooldown_ticks
        self.weapon_class = weapon_class
        self._cur_ticks = 0

    def tick(self):
        """One tick for the weapon"""
        self._cur_ticks -= 1

    def can_fire(self):
        return self._cur_ticks <= 0

    def fire(self):
        """Tries to fire the gun

        If the gun can fire, it will return a new instance of the class of the
        weapon. Else returns None
        
        """
        if self.can_fire():
            self._cur_ticks = self.cooldown_ticks
            return self.weapon_class()
        else:
            return None


class MachineGun(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = util.load_image("machine_gun.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.left += MACHINE_GUN_V
