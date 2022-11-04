# coding: utf-8

from setuptools import setup

REQUIRES = ['aiohttp', 'motor', 'requests', 'tornado', 'pycryptodome', 'pyjwt']

setup(
    name='vquant_utils',
    version='1.0.0',
    description='vquant_utils',
    platforms='Independant',
    zip_safe=False,
    install_requires=REQUIRES,
    packages=['vquant_utils']
)
