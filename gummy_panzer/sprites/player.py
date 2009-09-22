import pygame
import logging
from gummy_panzer import settings
from gummy_panzer.sprites import damageable, util, weapons, tractorbeam,effects

LOG = logging.getLogger(__name__)


PLAYER_CEILING = 0
PLAYER_FLOOR = int(settings.SCREEN_HEIGHT - 0.05 * settings.SCREEN_HEIGHT)
PLAYER_LEFT = 0
PLAYER_RIGHT = settings.SCREEN_WIDTH


ACCEL = 1
MAX_V = 15
PLAYER_MAX_HEALTH = 20


MACHINE_GUN_COOLDOWN = 7
MACHINE_GUN_CHARGE_TICKTIME = [20, 30, 40]


class _MovingState(object):
    STOPPED = 0
    PLUS = 1
    MINUS = -1


class Player(effects.SpriteSheet, damageable.Damageable):

    def __init__(self, *groups):
        sheet = util.load_image("dinosheet.png")
        image_size = (100, 100)
        effects.SpriteSheet.__init__(self, sheet, image_size, *groups)
        damageable.Damageable.__init__(self, PLAYER_MAX_HEALTH)
        self.energy = 0
        self._ms_x = _MovingState.STOPPED
        self._ms_y = _MovingState.STOPPED
        self._machine_gun_factory = weapons.ChargingWeaponFactory(
                                                  MACHINE_GUN_COOLDOWN,
                                                  weapons.MachineGun,
                                                  MACHINE_GUN_CHARGE_TICKTIME)
        self._weapons_state = {"machine_gun": False}
        self._tractor_beam = tractorbeam.TractorBeam(self)
        class _Velocity(object):
            x = 0
            y = 0
        self._velocity = _Velocity()

        self.drawc=0
        self.drawcount = 2

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, val):
        self.__energy = max(0, val)
        self.__energy = min(self.__energy, 100)

    def move_up(self):
        self._ms_y = _MovingState.MINUS

    def move_down(self):
        self._ms_y = _MovingState.PLUS

    def move_left(self):
        self._ms_x = _MovingState.MINUS

    def move_right(self):
        self._ms_x = _MovingState.PLUS

    def stop_horizontal(self):
        self._ms_x = _MovingState.STOPPED

    def stop_vertical(self):
        self._ms_y = _MovingState.STOPPED

    @staticmethod
    def _get_physics(current_position, current_velocity, moving_state):
        """Returns (new velocity, new x)"""

        # Figure out which way acceleration goes
        if moving_state == _MovingState.STOPPED:
            if current_velocity > 0:
                acceleration = -ACCEL
            elif current_velocity < 0:
                acceleration = ACCEL
            else:
                acceleration = 0
        elif moving_state == _MovingState.PLUS:
            acceleration = ACCEL
        else:
            acceleration = -ACCEL

        # Figure out new values
        current_position += current_velocity
        velocity = min(MAX_V, current_velocity + acceleration)
        velocity = max(-MAX_V, velocity + acceleration)
        if (moving_state == _MovingState.STOPPED and
                (velocity > 0 and current_velocity < 0 ) or
                (velocity < 0 and current_velocity > 0)):
            velocity = 0
        return (velocity, current_position)

    def handle_event(self, event):
        """Handles an event

        returns any Sprite's that should be added to the world
        
        """
        if event.type == pygame.KEYDOWN:
            # Parse movement keys
            if event.key == pygame.K_d:
                self.move_right()
            elif event.key == pygame.K_a:
                self.move_left()
            elif event.key == pygame.K_w:
                self.move_up()
            elif event.key == pygame.K_s:
                self.move_down()
            # Parse weapon keys
            elif event.key == pygame.K_SPACE:
                self._machine_gun_factory.charge()
            elif event.key == pygame.K_LSHIFT:
                self._tractor_beam.extending = True
                self._tractor_beam.retracting = False
        elif event.type == pygame.KEYUP:
            # Parse release of movement key
            if event.key in (pygame.K_a, pygame.K_d):
                self.stop_horizontal()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_a]:
                    self.move_left()
                elif keys_pressed[pygame.K_d]:
                    self.move_right()
            elif event.key in (pygame.K_w, pygame.K_s):
                self.stop_vertical()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_s]:
                    self.move_down()
                elif keys_pressed[pygame.K_w]:
                    self.move_up()
            # Parse release of weapon keys
            elif event.key == pygame.K_SPACE:
                self._machine_gun_factory.stop_charging()
                if self._machine_gun_factory.can_fire():
                    self._weapons_state["machine_gun"] = True
            elif event.key == pygame.K_LSHIFT:
                self._tractor_beam.extending = False
                self._tractor_beam.extended = False
                self._tractor_beam.retracting = True

    def update(self):
        """Updates positions of the player

        Also returns all projectiles that have been created or None
        
        """
        x, y = self.rect.topleft

        self._velocity.x, x = Player._get_physics(x,
                                                  self._velocity.x,
                                                  self._ms_x)
        self._velocity.y, y = Player._get_physics(y,
                                                  self._velocity.y,
                                                  self._ms_y)

        # Limit on the top left
        x = max(PLAYER_LEFT, x)
        y = max(PLAYER_CEILING, y)

        # Set location
        self.rect.topleft = x, y
        self.drawc+=1

        if self.drawc == self.drawcount:
            self.anim_frame = (self.anim_frame + 1) % 19
            self.drawc = 0
        # limit on the bottom right
        self.rect.right = min(self.rect.right, PLAYER_RIGHT)
        self.rect.bottom = min(self.rect.bottom, PLAYER_FLOOR)

        firing_weapons = []
        if self._weapons_state["machine_gun"]:
            firing_weapons.append(self._machine_gun_factory.fire())
            self._weapons_state["machine_gun"] = False
        firing_weapons = filter(lambda x: x is not None, firing_weapons)
        assert all(firing_weapons)

        for bullet in firing_weapons:
            if isinstance(bullet, weapons.Emp):
                bullet.rect.left = self.rect.right - 90
                bullet.rect.centery = self.rect.centery - 33
            else:
                bullet.rect.left = self.rect.right - 18
                bullet.rect.centery = self.rect.centery - 33

        self._machine_gun_factory.tick()
        self._tractor_beam.update(self)

        return firing_weapons




