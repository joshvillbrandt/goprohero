[![Build Status](https://travis-ci.org/joshvillbrandt/goprohero.svg?branch=master)](https://travis-ci.org/joshvillbrandt/goprohero) [![Documentation Status](https://readthedocs.org/projects/goprohero/badge/?version=latest)](http://goprohero.readthedocs.org/en/latest/)

# goprohero

A Python library for controlling GoPro cameras over http.

## Description

This package includes a both a library and a command line interface that can interface with GoPro HERO3, HERO3+, and HERO4 cameras over http.

The library can be used to set any of the configurable options of the camera and can also interpret the camera's status details. OpenCV (if installed) is used to open the live stream and save a single frame.

The command line interface utilizes the [wireless](https://github.com/joshvillbrandt/wireless) library to control one or more cameras from a single command.

For more advanced management of multiple cameras, check out the [GoProController](https://github.com/joshvillbrandt/GoProController) and [GoProControllerUI](https://github.com/joshvillbrandt/GoProControllerUI) packages which allow for command queuing and status history as well as an interface to view the live stream image captures.

Requirements:

* GoPro HERO3, GoPro HERO3+, or GoPro HERO4
* A computer with a wireless card
* (optional) OpenCV

## Documentation

Documentation is available on [readthedocs.org](http://goprohero.readthedocs.org/en/latest/).
