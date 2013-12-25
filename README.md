GoProController
===============

A lightweight Python class for interfacing with multiple GoPros.

## Description

This class can interfaces with GoPro cameras in their wifi ad-hoc mode (aka GoPro App mode.) When used with multiple cameras, the class will automatically jump between networks. GoProController can also take snapshots from the camera's live stream. OpenCV is used to open the stream and save a single frame.

## Installation

GoProController is developed and tested on Ubuntu. To install the prerequisites, run the following:

    sudo apt-get install python-numpy python-opencv

## Todo List

* make this available via pip or at least use a requirements.txt file
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
