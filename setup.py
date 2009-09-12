# bootstrap setuptools if necessary
from ez_setup import use_setuptools
use_setuptools()

VERSION=0.1

from setuptools import setup

setup(name="gummy_panzer",
        version=VERSION,
        packages=["gummy_panzer", "gummy_panzer.sprites"],
        )

