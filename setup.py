#!/usr/bin/env python

from setuptools import setup

setup(
    name='goprocontroller',
    version='0.2.0',
    description='A lightweight Python class for interfacing with multiple ' +
    'GoPros.',
    long_description=open('README.md').read(),
    url='https://github.com/joshvillbrandt/GoProController',
    author='Josh Villbrandt',
    author_email='josh@javconcepts.com',
    license=open('LICENSE').read(),
    packages=['goprocontroller'],
    install_requires=[
        'numpy'
    ],
    scripts=[],
    test_suite='tests',
    zip_safe=False
)
