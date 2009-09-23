from gummy_panzer import settings
from gummy_panzer.sprites import wave, enemies

def _wave_one(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('enemy_sprite.png', (150, 300)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

def _wave_two(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

def _wave_three(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    return w

def _wave_four(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 200)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 400)))
    return w

def _wave_five(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 200)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    return w

def _wave_six(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 200)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 400)))
    return w

def _wave_seven(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 200)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

_WAVE_FUNCTIONS = ((_wave_one, 200),
        (_wave_two, 800),
        (_wave_three, 1400),
        (_wave_four, 2000),
        (_wave_five, 2600),
        (_wave_six, 3200),
        (_wave_seven, 3800),
        )

def waves():
    waves = []
    for wave_fn, time in _WAVE_FUNCTIONS:
        waves.append(wave_fn(time))
    return waves
