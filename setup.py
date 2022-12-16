# coding: utf-8

from setuptools import setup

REQUIRES = ['aiohttp', 'aiosmtplib', 'motor', 'requests', 'tornado', 'pycryptodome', 'pyjwt']

setup(
    name='vquant_utils',
    version='1.12.16',
    description='vquant_utils',
    platforms='Independant',
    zip_safe=False,
    install_requires=REQUIRES,
    packages=['vquant_utils']
)
