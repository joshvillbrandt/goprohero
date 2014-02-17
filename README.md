# GoProController

A lightweight Python class for interfacing with multiple GoPros.

## Description

This class can interfaces with GoPro cameras in their wifi ad-hoc mode (aka GoPro iOS App mode.) When used with multiple cameras, the class will automatically jump between networks. GoProController can also take snapshots from the camera's live stream. OpenCV is used to open the stream and save a single frame.

## Background

My use case for this code is to remotely configure and check the status of about ten GoPro cameras from afar. I've built a tiny BeagleBone PC running Ubuntu that runs this script and [GoProApp](https://github.com/joshvillbrandt/GoProApp) via Apache. The PC has a wifi adapter to communicate with the GoPros and talks back to the primary network over wired Ethernet.

During the development of this script, we discovered that the GoPro can work in entirely two different Wifi scnearios. This script takes advantage of the camera's ability to connect to an iOS app. In this scenario, the camera creates an ad-hoc network that a client can connect to. The cameras can also be configured to jump on to an infrastructure network. The intended scenario here is for use with GoPro's remote to control multiple cameras simultaneously. From my limited testing, it seems that the remote-to-camera communication is much more limited. The obvious advantage though is that one doesn't have to jump on different wifi networks to talk to multiple cameras.

At the moment, I am not pursueing additional research into the infrastructure mode of the cameras. However, if someone can provide me an example code controlling two cameras without jumping networks, then I'm happy to change this code around. Check out my [Infrastructure Wifi Research](Infrastructure Wifi Research.md) from last September for a good starting point on this approach.

## Installation

GoProController is developed and tested on Ubuntu. To install the prerequisites, run the following:

```bash
sudo apt-get install python-numpy python-opencv git
```

Then clone the repo:

```bash
git clone https://github.com/joshvillbrandt/GoProController.git
```

You can use this module in your own code by using something like this:

```python
from GoProController import GoProController
c = GoProController()
c.test()
```

## Todo List

* hack the infrastructure network that the GoPro Remote makes and learn how to have GoPros on only one network
* look into the wifi_networks list that in the settings.in file that is present when updating GoPro firmware
* revamp crappy wifi connect code
* respond better to keyboard interrupts
* still some information in the status byte streams i haven't translated... I don't really need the rest though
* openCV functions can get a segfault if the wifi connection is spotty - that stucks
* GoPro 3 wifi sometimes shuts off when charging via USB even though the wifi LED is still flashing
* "charging" indicator might not be accurate with an extra battery pack.

## Contributions

Pull requests are welcomed!
