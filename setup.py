#!/usr/bin/env python

from setuptools import setup

setup(
    name='gopro',
    version='0.2.0-dev2',
    description='A Python library for controlling GoPro cameras over http.',
    long_description=open('README.md').read(),
    url='https://github.com/joshvillbrandt/gopro',
    author='Josh Villbrandt',
    author_email='josh@javconcepts.com',
    license=open('LICENSE').read(),
    packages=['gopro'],
    setup_requires=[
        'tox',
        'nose',
        'flake8'
    ],
    install_requires=[
        'PIL',
        'colorama'
    ],
    scripts=[],
    test_suite='tests',
    zip_safe=False
)
