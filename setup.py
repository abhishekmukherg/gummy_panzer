# bootstrap setuptools if necessary
from ez_setup import use_setuptools
use_setuptools()
#from distutils.core import setup

VERSION=0.1

from setuptools import setup

setup(name="gummy_panzer",
        version=VERSION,
        packages=["gummy_panzer", "gummy_panzer.sprites"],
        scripts=["main.py"],
        install_requires = ['pygame'],
        package_data = {
            'gummy_panzer': ['images/*.png', 'Sounds/*.ogg'],
        }
)

