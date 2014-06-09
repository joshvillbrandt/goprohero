# GoProController

A lightweight Python class for interfacing with multiple GoPros.

## Description

Warning: The HEAD commit is unstable right now. Please use the v0.1.1 tag.

This class can interfaces with GoPro cameras in their wifi ad-hoc mode (aka GoPro iOS App mode.) When used with multiple cameras, the class will automatically jump between networks. GoProController can also take snapshots from the camera's live stream. OpenCV is used to open the stream and save a single frame.

## Background

My use case for this code is to remotely configure and check the status of about ten GoPro cameras from afar. I've built a tiny BeagleBone PC running Ubuntu that runs this script and [GoProApp](https://github.com/joshvillbrandt/GoProApp) via Apache. The PC has a wifi adapter to communicate with the GoPros and talks back to the primary network over wired Ethernet.

During the development of this script, we discovered that the GoPro can work in entirely two different Wifi scnearios. This script takes advantage of the camera's ability to connect to an iOS app. In this scenario, the camera creates an ad-hoc network that a client can connect to. The cameras can also be configured to jump on to an infrastructure network. The intended scenario here is for use with GoPro's remote to control multiple cameras simultaneously. From my limited testing, it seems that the remote-to-camera communication is much more limited. The obvious advantage though is that one doesn't have to jump on different wifi networks to talk to multiple cameras.

At the moment, I am not pursueing additional research into the infrastructure mode of the cameras. However, if someone can provide me an example code controlling two cameras without jumping networks, then I'm happy to change this code around. Check out my [Infrastructure Wifi Research](Infrastructure Wifi Research.md) from last September for a good starting point on this approach.

## Installation

GoProController is developed and tested on Ubuntu 12.04.

```bash
sudo apt-get install python-opencv
sudo pip install goprocontroller
```

## Usage

If you only need to control one GoPro, try this:

```python
from goprocontroller import GoPro
camera = GoPro(password='set_during_firmware_install')
camera.sendCommand('record_on')
status = camera.getStatus()
```

If you need to control many GoPros, put them into the ad-hoc mode and try this:

```python
# tbd
```

## API

GoPro:

* `GoPro(ip, password)` - initialize a camera object
* `setPassword(password)` - change the password of a camera object
* `getStatus()` - get status packets and translate them
* `getImage()` - get an image and return it as a base64-encoded PNG string
* `sendCommand(command)` - send one of the support commands ('power_off', 'power_on', 'record_off', 'record_on', 'mode_video', 'mode_still')

AdHocController:

* tbd

## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.2.0 - 2014/06/09

* Refactor code to separate gopro interface from wifi SSID swapping.
* Add to PyPI.
* Now passes Flake8.

### v0.1.1 - 2014/02/17

* Add better documentation.

### v0.1.0 - 2013/10/30

* Initial release.

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

Pull requests are welcomed!
