import pygame
import logging
import pkg_resources
import os
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects


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
        self.sfx=pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "laser.ogg")))
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
            self.sfx.play(loops=0)
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
        self.sfx=pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "charge.ogg")))
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
        i = 0
        LOG.debug("Charge ticks: %d" % self._charge)
        for value in self.charge_times:
            self._charge -= value
            # Done Charging
            if self._charge <= 0:
                break
            i += 1
        LOG.debug("Resultant power: %d" % i)
        self._charge = 0
        if i < 3:
            return MachineGun(i)
        else:
            return Emp()


class MachineGun(pygame.sprite.Sprite):

    def __init__(self, charge, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        if charge == 0:
            image = "machine_gun.png"
        elif charge < 3 and charge > 0:
            image = "charged_gun.png"
        else:
            image = "emp_blast.png"
        # self.sfx=pygame.mixer.sound("../Sounds/laser.wav")
        self.sfx=pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "laser.ogg")))
        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.charge = charge
        LOG.debug("Creating machine gun with charge %d" % charge)

    @property
    def damage_done(self):
        d = (1, 3, 7, 15)[self.charge]
        print d
        return d

    def update(self):
        self.rect.left += MACHINE_GUN_V


class Emp(effects.SpriteSheet):

    EMP_TICK_LIMITS = (1, 4, 8, 12, 16)

    def __init__(self, *groups):
        effects.SpriteSheet.__init__(self, util.load_image("emp_blast.png"),
                (200, 200), *groups)
        self.sfx=pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
        os.path.join("Sounds", "emp.ogg")))
        self.exploding = False
        self.emp_tick = 0

    @property
    def explosion_level(self):
        return len(Emp.EMP_TICK_LIMITS) - len(filter(lambda x: x,
            map(lambda x: self.emp_tick < x, Emp.EMP_TICK_LIMITS)))

    def update(self):
        if self.exploding:
            self.emp_tick += 1

            self.anim_frame = self.explosion_level
            self.rect.x += int(0.15 * MACHINE_GUN_V)
            if self.anim_frame >= len(Emp.EMP_TICK_LIMITS):
                super(Emp, self).kill()
        else:
            self.rect.left += int(0.5 * MACHINE_GUN_V)
        super(Emp, self).update()

    def kill(self):
        self.exploding = True


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
