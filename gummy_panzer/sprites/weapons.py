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
    SFX_LASER = "laser.ogg"
    SFX_CHARGE = "charge.ogg"
    SFX_EMPFIRE = "empfire.ogg"
    SFX_EMPTRAVEL="emptravel.ogg"
    SFX_EMPEXPLODE="empexplode.ogg"
    SFX_CHARGING="charging.ogg"
else:
    SFX_LASER, SFX_CHARGE, SFX_EMPTRAVEL,SFX_EMPFIRE,SFX_EMPEXPLODE = None, None, None,None, None
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

        If the gun can fire, it will return a neaw instance of the class of the
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
        return self.weapon_class(i)


class MachineGun(pygame.sprite.Sprite):

    def __init__(self, charge, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        if charge == 0:
            if SFX_LASER is not None:
                sound = SFX_LASER
            image = "chargebullet01_3.png"
        elif charge== 1:
            if SFX_CHARGE is not None:
                sound = SFX_CHARGE
            image = "chargebullet02_2.png"
        else:
            if SFX_CHARGE is not None:
                sound = SFX_CHARGE
            image = "chargebullet03_2.png"
            
        self.sfx= pygame.mixer.Sound(pkg_resources.resource_stream("gummy_panzer",
            os.path.join("Sounds", sound)))
        self.sfx.play()

        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.charge = charge
        self.velocity = (MACHINE_GUN_V, 0)
        self.acceleration = (0, 0)
        LOG.debug("Creating machine gun with charge %d" % charge)

    @property
    def damage_done(self):
        d = (1, 5, 5, 10)[self.charge]
        LOG.info("Charge:%d / Damage:%d" % (self.charge, d))
        return d

    def kill(self):
        self.sfx.stop()
        super(MachineGun, self).kill()

    def update(self):
        self.rect.left += self.velocity[0]
        self.rect.top += self.velocity[1]
        self.velocity = (self.velocity[0] + self.acceleration[0],
                         self.velocity[1] + self.acceleration[1])


class Emp(effects.SpriteSheet):

    EMP_TICK_LIMITS = (1, 4, 7, 10, 12, 14, 16)

    def __init__(self, charge, *groups):
        effects.SpriteSheet.__init__(self, util.load_image("emp_blast.png"),
                (200, 200), *groups)

        self.exploding = False
        self.charge = charge * 20
        self.emp_tick = 0
        self.damage_done = 20
        if SFX_CHARGE is not None:
            sound = SFX_EMPFIRE
            self.sfx= pygame.mixer.Sound(
                pkg_resources.resource_stream("gummy_panzer",
                os.path.join("Sounds", sound)))
        if SFX_EMPTRAVEL is not None:
            self.sfx.play()
            self.sfx= pygame.mixer.Sound(pkg_resources.resource_stream(
                "gummy_panzer", os.path.join("Sounds", SFX_EMPTRAVEL)))
            self.sfx.play(-1)
            
        LOG.info("Emp created with charge: %d" % self.charge)

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
        elif self.charge <= 0:
            self.exploding = True
        else:
            self.rect.left += int(0.5 * MACHINE_GUN_V)
            self.charge -= 1
        super(Emp, self).update()

    def kill(self):
        self.sfx.stop()
        self.sfx=pygame.mixer.Sound(pkg_resources.resource_stream(
            "gummy_panzer", os.path.join("Sounds", SFX_EMPEXPLODE)))
        self.sfx.play()
        self.exploding = True


class Laser(pygame.sprite.Sprite):

    CHARGE_TIME = 25
    TIMEOUT = 10

    damage_done = 15

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.ticks = 0
        self.image = util.load_image("lazercharge.png")
        self.rect = self.image.get_rect()

    @property
    def charged(self):
        return self.ticks >= Laser.CHARGE_TIME

    def update(self):
        if self.ticks >= Laser.CHARGE_TIME + Laser.TIMEOUT:
            self.kill()
        elif self.ticks >= Laser.CHARGE_TIME:
            image = util.load_image("laser.png")
            rect = image.get_rect()
            rect.centery = self.rect.centery
            rect.right = self.rect.right
            self.image = image
            self.rect = rect
        self.ticks += 1


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
