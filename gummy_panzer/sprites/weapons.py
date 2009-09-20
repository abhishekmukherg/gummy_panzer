import pygame
import logging
from gummy_panzer.sprites import util


MACHINE_GUN_V = 20
LOG = logging.getLogger(__name__)


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
            return self._create_weapon()
        else:
            return None

    def _create_weapon(self):
        return self.weapon_class()

class ChargingWeaponFactory(WeaponFactory):

    def __init__(self, cooldown_ticks, weapon_class, charge_times):
        """Creates a charging weapon class

        charge_times is something that can be iterated over multiple times and
        holds the number of ticks per charge level

        weapon_class should take one argument, the charge level

        """
        WeaponFactory.__init__(self, cooldown_ticks, weapon_class)
        self._charge = 0
        self.charging = False
        self.charge_times = charge_times

    def tick(self):
        if self.charging:
            self._charge += 1
        else:
            super(ChargingWeaponFactory, self).tick()

    def charge(self):
        assert not self.charging
        self.charging = True

    def stop_charging(self):
        self.charging = False

    def _create_weapon(self):
        """
        >>> class Foo(object):
        ...     def __init__(self, i): self.i = i
        >>> c = ChargingWeaponFactory(5, Foo, [0, 1, 5, 10])
        >>> c.can_fire()
        True
        >>> c.charge()
        >>> c.stop_charging()
        >>> c.fire() is not None
        Charge ticks: 0 => 1
        True
        >>> c._cur_ticks = 0
        >>> c.charge()
        >>> c.tick()
        >>> c.stop_charging()
        >>> c.fire() is not None
        Charge ticks: 1 => 2
        True
        """

        i = 0
        LOG.debug("Charge ticks: %d" % self._charge)
        for value in self.charge_times:
            self._charge -= value
            i += 1
            # Done Charging
            if self._charge <= 0:
                break
        LOG.debug("Resultant power: %d" % i)
        self._charge = 0
        return self.weapon_class(i)


class MachineGun(pygame.sprite.Sprite):

    def __init__(self, charge, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        image = "machine_gun.png" if charge <= 2 else "charged_gun.png"
        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.charge = charge
        LOG.debug("Creating machine gun with charge %d" % charge)

    def update(self):
        self.rect.left += MACHINE_GUN_V


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
