import pygame
import logging
import pkg_resources
import os
from gummy_panzer import settings
from gummy_panzer.sprites import util, effects


MACHINE_GUN_V = 20
LOG = logging.getLogger(__name__)

pygame.mixer.init()
if pygame.mixer.get_init() is not None:
    SFX_LASER = pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "laser.ogg")))
    SFX_CHARGE = pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "charge.ogg")))
    SFX_EMP = pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", "emp.ogg")))
else:
    SFX_LASER, SFX_CHARGE, SFX_EMP = None, None, None
    LOG.error("Could not use mixer")


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
            if SFX_LASER is not None:
                sound=SFX_LASER
            image = "machine_gun.png"
        elif charge < 3 and charge > 0:
            if SFX_CHARGE is not None:
                sound=SFX_CHARGE
            image = "charged_gun.png"
        else:
            if SFX_CHARGE is not None:
                sound=SFX_CHARGE
            image = "emp_blast.png"
            
            
        self.sfx=sound
        self.sfx.play(loops=0)

        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.charge = charge
        self.velocity = (MACHINE_GUN_V, 0)
        self.acceleration = (0, 0)
        LOG.debug("Creating machine gun with charge %d" % charge)

    @property
    def damage_done(self):
        d = (1, 3, 3, 10)[self.charge]
        return d

    def update(self):
        self.rect.left += self.velocity[0]
        self.rect.top += self.velocity[1]
        self.velocity = (self.velocity[0] + self.acceleration[0],
                         self.velocity[1] + self.acceleration[1])


class Emp(effects.SpriteSheet):

    EMP_TICK_LIMITS = (1, 4, 7, 10, 12, 14, 16)


    def __init__(self, *groups):
        effects.SpriteSheet.__init__(self, util.load_image("emp_blast.png"),
                (200, 200), *groups)

        self.exploding = False
        self.emp_tick = 0
        self.damage_done = 20

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
