import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='marquee',
    version='0.0.1',
    author='Gary Johnson',
    author_email = 'gary@gjtt.com',
    description = 'Client for blasting fullscreen gifs',
    license = 'MIT',
    packages = ['marquee'],
    )
