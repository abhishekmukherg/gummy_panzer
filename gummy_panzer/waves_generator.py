from gummy_panzer import settings
from gummy_panzer.sprites import wave, enemies

def _wave_one(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 100, 290)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

def _wave_two(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

def _wave_three(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    return w

def _wave_four(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 190)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 390)))
    return w

def _wave_five(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 190)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    return w

def _wave_six(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 190)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 390)))
    return w

def _wave_seven(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 190)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w

def _wave_eight(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH + 100, 90)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH + 100, 190)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH - 50, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 50, 485)))
    return w

def _wave_nine(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 100, 90)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH + 200, 190)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 100, 485)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH + 200, 485)))
    return w
    
def _wave_ten(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 340)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 440)))
    w.add(enemies.Enemy('bernard.png', (settings.SCREEN_WIDTH, 485)))
    return w
    
def _wave_eleven(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 90)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 190)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 290)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 390)))   
    return w
    
def _wave_twelve(time):
    w = wave.Wave(time)
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH - 100, 75)))
    w.add(enemies.Enemy('gertrude01.png', (settings.SCREEN_WIDTH, 340)))
    w.add(enemies.Enemy('fred.png', (settings.SCREEN_WIDTH, 440)))   
    return w


_WAVE_FUNCTIONS = ((_wave_one, 100),
        (_wave_two, 600),
        (_wave_three, 1200),
        (_wave_four, 1800),
        (_wave_five, 2400),
        (_wave_six, 3000),
        (_wave_seven, 3600),
        (_wave_eight, 4200),
        (_wave_nine, 5000),
        (_wave_five, 5600),
        (_wave_six, 5200),
        (_wave_ten, 6200),
        (_wave_nine, 6800),
        (_wave_four, 7600),
        (_wave_five, 8200),
        (_wave_six, 8800),
        (_wave_ten, 9600),
        (_wave_three, 10200),
        (_wave_eleven, 11000),
        (_wave_twelve, 11500),
        (_wave_twelve, 12000),
        (_wave_eight, 12500),
        (_wave_one, 13000),
        (_wave_ten, 13400),
        (_wave_five, 14200),
        (_wave_six, 14700),
        (_wave_twelve, 15200),
        (_wave_nine, 16000),
        (_wave_five, 16500),
        (_wave_eleven, 17000),
        (_wave_ten, 17500),
        )

def waves():
    waves = []
    for wave_fn, time in _WAVE_FUNCTIONS:
        waves.append(wave_fn(time))
    return waves
