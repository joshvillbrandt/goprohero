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

## Background

My original use case for this code is to remotely configure and check the status of approximately ten GoPro HERO3 cameras from afar. We built a tiny BeagleBone PC running Ubuntu that uses this library along with the [GoProController](https://github.com/joshvillbrandt/GoProController). The BeagleBone PC has a wifi adapter to communicate with the GoPros and talks back to the primary network over wired Ethernet.

During the development of this library, we discovered that there are two entirely different methods for communicating with a GoPro wirelessly. The first method is an HTTP protocol  intended for the iOS and Android applications. In this scenario, the camera creates an ad-hoc network that a client device can connect to. A second method is available for the GoPro Wifi Remote. In this scenario, the remote creates an infrastructure network that multiple GoPros can connect to. While the infrastructure mode would seem ideal for communicating with multiple cameras simultaneously, it is much more difficult to interface with (it doesn't appear to be using standard TCP/IP) and lacks the complete functionality that the first method has (can't download files or view the live preview.) For these reasons, this library uses the ad-hoc/HTTP method.

This project also produced the [wireless](https://github.com/joshvillbrandt/wireless) Python library to simply connecting to multiple cameras across platforms.

## Quick Start

Install the `goprohero` library:

```bash
sudo pip install goprohero
```

A typical usage looks like this:

```python
from goprohero import GoProHero
camera = GoProHero(password='password')
camera.command('record', 'on')
status = camera.status()
```

## Todo List

* method to list photos and videos
* method to download photos and videos
* still some information in the status byte streams i haven't translated... I don't really need the rest though
* add more commands

## Contributions

Pull requests to the `develop` branch are welcomed!
