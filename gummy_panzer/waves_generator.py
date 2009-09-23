from gummy_panzer import settings
from gummy_panzer.sprites import wave, enemies

def _wave_one(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 100, 300)))
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
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH + 100, 100)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH + 100, 200)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH - 50, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 50, 485)))
    return w

def _wave_nine(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 100, 100)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 200, 200)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 100, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 200, 485)))
    return w
    
def _wave_ten(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 350)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 450)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w
    
def _wave_eleven(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 100)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 200)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 300)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 400)))   
    return w
    
def _wave_twelve(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH - 100, 75)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 350)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 450)))   
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
        (_wave_ten, 7200),
        (_wave_nine, 8000),
        (_wave_four, 9000),
        (_wave_five, 9200),
        (_wave_six, 9400),
        (_wave_ten, 10200),
        (_wave_three, 11000),
        (_wave_eleven, 11500),
        (_wave_twelve, 12000),
        (_wave_twelve, 13000),
        (_wave_eight, 13500),
        (_wave_one, 14000),
        (_wave_ten, 14400),
        (_wave_five, 15500),
        (_wave_six, 16000),
        (_wave_twelve, 16500),
        (_wave_nine, 18000),
        (_wave_five, 18500),
        (_wave_eleven, 19000),
        (_wave_ten, 19500),
        )

def waves():
    waves = []
    for wave_fn, time in _WAVE_FUNCTIONS:
        waves.append(wave_fn(time))
    return waves
