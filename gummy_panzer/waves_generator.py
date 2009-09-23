from gummy_panzer import settings
from gummy_panzer.sprites import wave, enemies

def _wave_one(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (900, 300)))
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

def _wave_eight(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (900, 100)))
    w.add(enemies.Enemy('fred.png', (900, 200)))
    w.add(enemies.Enemy('bernard.png', (750, 485)))
    w.add(enemies.Enemy('bernard.png', (850, 485)))
    return w

def _wave_nine(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (900, 100)))
    w.add(enemies.Enemy('gertrude01.png', (1000, 200)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    w.add(enemies.Enemy('bernard.png', (900, 485)))
    w.add(enemies.Enemy('bernard.png', (1000, 485)))
    return w
    
def _wave_ten(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 350)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 450)))

    w.add(enemies.Enemy('bernard.png', (1000, 485)))
    return w


_WAVE_FUNCTIONS = ((_wave_one, 200),
        (_wave_two, 800),
        (_wave_three, 1400),
        (_wave_four, 2000),
        (_wave_five, 2600),
        (_wave_six, 3200),
        (_wave_seven, 3800),
        (_wave_eight, 4400),
        (_wave_nine, 5400),
        (_wave_five, 6000),
        (_wave_six, 6600),
        (_wave_one, 7200),
        (_wave_nine, 8000),
        (_wave_four, 9000),
        (_wave_five, 9200),
        (_wave_six, 9400),
        (_wave_ten, 10200),
        (_wave_three, 11000),
        )

def waves():
    waves = []
    for wave_fn, time in _WAVE_FUNCTIONS:
        waves.append(wave_fn(time))
    return waves
