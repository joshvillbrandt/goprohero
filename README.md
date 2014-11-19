[![Build Status](https://travis-ci.org/joshvillbrandt/gopro.svg?branch=master)](https://travis-ci.org/joshvillbrandt/gopro)

# gopro

A Python library for controlling GoPro cameras over http.

## Description

This library can interface with a GoPro camera on the local network. Once conneced, full control of the camera and all configuration details are available. OpenCV is used to open the stream and save a single frame.

Requirements:

* GoPro HERO3, GoPro HERO3+, or GoPro HERO4
* A computer with a wireless card

## Background

My original use case for this code is to remotely configure and check the status of about ten GoPro HERO3 cameras from afar. We built a tiny BeagleBone PC running Ubuntu that runs this script along with the [GoProController](https://github.com/joshvillbrandt/GoProController). The BeagleBone PC has a wifi adapter to communicate with the GoPros and talks back to the primary network over wired Ethernet.

During the development of this script, we discovered that the GoPro can work in entirely two different Wifi scnearios. This script takes advantage of the camera's ability to connect to an iOS app. In this scenario, the camera creates an ad-hoc network that a client can connect to. The cameras can also be configured to jump on to an infrastructure network. The intended scenario here is for use with GoPro's remote to control multiple cameras simultaneously. From my limited testing, it seems that the remote-to-camera communication is much more limited. The obvious advantage though is that one doesn't have to jump on different wifi networks to talk to multiple cameras.

At the moment, I am not pursueing additional research into the infrastructure mode of the cameras. However, if someone can provide me an example code controlling two cameras without jumping networks, then I'm happy to change this code around. Check out my [Infrastructure Wifi Research](Infrastructure Wifi Research.md) from last September for a good starting point on this approach.

## Setup

Install the `gopro` library using pip:

```bash
sudo pip install gopro
```

To connect with a GoPro, you will need to have the camera on the local network. This can be accomplished by:

1. Turning on the GoPro wireless "app" mode - this instructs the camera to create an AdHoc wireless network
1. Connecting the computer running this library to the camera's network

This connection process can be automated with the [GoProController](https://github.com/joshvillbrandt/GoProController). Once connect

## Usage

A typical usage looks like this:

```python
from gopro import GoPro
camera = GoPro(password='password')
camera.sendCommand('record_on')
status = camera.getStatus()
```

## API

* `camera = GoPro(password, ip='10.5.5.9')` - initialize a camera object
* `camera.setPassword(password)` - change the password of a camera object
* `camera.getStatus()` - get status packets and translate them
* `camera.getImage()` - get an image and return it as a base64-encoded PNG string
* `camera.sendCommand(command)` - send one of the supported commands
  * avialable commands are `power_off`, `power_on`, `record_off`, `record_on`, `mode_video`, and `mode_still`


## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.2.0 - tbd [develop branch]

* Renamed project from `GoProController` to `gopro`
* Refactored wifi code out of the project leaving only the GoPro commanding and status logic
* Added support for HERO3+ and HERO4 cameras
* Added to PyPI
* Now passes Flake8

### v0.1.1 - 2014/02/17

* Added better documentation

### v0.1.0 - 2013/10/30

* Initial release

## Todo List

* hack the infrastructure network that the GoPro Remote makes and learn how to have GoPros on only one network
 * look into the wifi_networks list that in the settings.in file that is present when updating GoPro firmware
* revamp crappy wifi connect code
* respond better to keyboard interrupts
* still some information in the status byte streams i haven't translated... I don't really need the rest though
* openCV functions can get a segfault if the wifi connection is spotty - that sucks
* GoPro 3 wifi sometimes shuts off when charging via USB even though the wifi LED is still flashing
* "charging" indicator might not be accurate with an extra battery pack.
* OpenCV + virtualenv: http://redesygn.com/jekyll/testing/2014/01/12/install-opencv-numpy-scipy-virtualenv-ubuntu-server.html

## Contributions

Pull requests to the `develop` branch are welcomed!
