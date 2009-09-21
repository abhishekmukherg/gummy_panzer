class Damageable(object):

    """
    A class that has health. I guess
    """
    
    def __init__(self, max_health):
        self.health = max_health
        self.max_health = max_health

    def damage(self, damage):
        self.health -= damage
        return self.is_dead()

    def is_dead(self):
        return self.health <= 0

