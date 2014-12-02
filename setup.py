#!/usr/bin/env python

from setuptools import setup

# auto-convert README.md
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, OSError):
    # we'll just use the poorly formatted Markdown file instead
    long_description = open('README.md').read()

setup(
    name='goprohero',
    version='0.2.5',
    description='A Python library for controlling GoPro cameras over http.',
    long_description=long_description,
    url='https://github.com/joshvillbrandt/gopro',
    author='Josh Villbrandt',
    author_email='josh@javconcepts.com',
    license=open('LICENSE').read(),
    packages=['goprohero'],
    setup_requires=[
        'tox',
        'nose',
        'flake8'
    ],
    install_requires=[
        'Pillow',
        'wireless',
        'colorama'
    ],
    scripts=['scripts/goproctl'],
    test_suite='tests',
    zip_safe=False
)
