import pygame
import logging
import random
from . import enemy_info, damageable, util, effects
from .. import settings

class wave():
    def __init__(self, distance):
        self.distance = distance