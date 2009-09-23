class Damageable(object):

    """
    A class that has health. I guess
    """
    
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val):
        self.__health = min(val, self.max_health)

    def damage(self, damage):
        self.health -= damage
        return self.is_dead()

    def is_dead(self):
        return self.health <= 0

