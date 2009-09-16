import pygame
from . import util
from . import weapons
from .. import settings

PLAYER_CEILING = int(0.1 * settings.SCREEN_HEIGHT)
PLAYER_FLOOR = int(settings.SCREEN_HEIGHT - 0.1 * settings.SCREEN_HEIGHT)
PLAYER_LEFT = 0
PLAYER_RIGHT = settings.SCREEN_WIDTH

ACCEL = 2
MAX_V = 20

MACHINE_GUN_COOLDOWN = 10

class _MovingState(object):
    STOPPED = 0
    PLUS = 1
    MINUS = -1

class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = util.load_image("player.png")
        self.rect = self.image.get_rect()
        self._ms_x = _MovingState.STOPPED
        self._ms_y = _MovingState.STOPPED
        self._machine_gun_factory = weapons.WeaponFactory(MACHINE_GUN_COOLDOWN,
                                                          weapons.MachineGun)
        class _Velocity(object):
            x = 0
            y = 0
        self._velocity = _Velocity()

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
            if event.key == pygame.K_d:
                self.move_right()
            elif event.key == pygame.K_a:
                self.move_left()
            elif event.key == pygame.K_w:
                self.move_up()
            elif event.key == pygame.K_s:
                self.move_down()
            elif event.key == pygame.K_SPACE:
                bullet = self._machine_gun_factory.fire()
                if bullet:
                    return bullet
        elif event.type == pygame.KEYUP:
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

    def update(self):
        x, y = self.rect.topleft

        self._velocity.x, x = Player._get_physics(x,
                                                  self._velocity.x,
                                                  self._ms_x)
        self._velocity.y, y = Player._get_physics(y,
                                                  self._velocity.y,
                                                  self._ms_y)

        x = max(PLAYER_LEFT, x)
        y = max(PLAYER_CEILING, y)

        self.rect.topleft = x, y

        self.rect.right = min(self.rect.right, PLAYER_RIGHT)
        self.rect.bottom = min(self.rect.bottom, PLAYER_FLOOR)
