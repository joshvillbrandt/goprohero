[![Build Status](https://travis-ci.org/joshvillbrandt/gopro.svg?branch=master)](https://travis-ci.org/joshvillbrandt/gopro) [![Documentation Status](https://readthedocs.org/projects/gopro/badge/?version=latest)](https://readthedocs.org/projects/gopro/?badge=latest)

# gopro

A Python library for controlling GoPro cameras over http.

## Description

This library can interface with a GoPro camera on the local network. Once connected, full control of the camera and all configuration details are available. OpenCV (if installed) is used to open the live stream and save a single frame.

Requirements:

* GoPro HERO3, GoPro HERO3+, or GoPro HERO4
* A computer with a wireless card
* (optional) OpenCV

## Background

My original use case for this code is to remotely configure and check the status of approximately ten GoPro HERO3 cameras from afar. We built a tiny BeagleBone PC running Ubuntu that uses this library along with the [GoProController](https://github.com/joshvillbrandt/GoProController). The BeagleBone PC has a wifi adapter to communicate with the GoPros and talks back to the primary network over wired Ethernet.

During the development of this library, we discovered that there are two entirely different methods for communicating with a GoPro wirelessly. The first method is an HTTP protocol  intended for the iOS and Android applications. In this scenario, the camera creates an ad-hoc network that a client device can connect to. A second method is available for the GoPro Wifi Remote. In this scenario, the remote creates an infrastructure network that multiple GoPros can connect to. While the infrastructure mode would seem ideal for communicating with multiple cameras simultaneously, it is much more difficult to interface with (it doesn't appear to be using standard TCP/IP) and lacks the complete functionality that the first method has (can't download files or view the live preview.) For these reasons, this library uses the ad-hoc/HTTP method.

This project also produced the [wireless](https://github.com/joshvillbrandt/wireless) Python library to simply connecting to multiple cameras across platforms.

## Setup

Install the `gopro` library and optional OpenCV library:

```bash
# sudo pip install gopro # working to put this into PyPI, but it isn't there yet...
git clone https://github.com/joshvillbrandt/gopro
cd gopro
sudo python setup.py install
```

To connect with a GoPro, you will need to have the camera on the local network. This can be accomplished by:

1. Turning on the GoPro wireless "app" mode - this instructs the camera to create an AdHoc wireless network
1. Connecting the computer running this library to the camera's network

This connection process can be automated with the [GoProController](https://github.com/joshvillbrandt/GoProController). Once connect

### Live Stream Image Capture

Some additional setup is required to capture a snapshot of the camera's live stream.

In Ubuntu 14.04, you'll need to install opencv and the [prereqs for Pillow](http://pillow.readthedocs.org/installation.html#linux-installation):

```bash
sudo apt-get install python-opencv
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
sudo pip uninstall Pillow; sudo pip install Pillow
sudo
```

For Mac, follow [this guide](https://jjyap.wordpress.com/2014/05/24/installing-opencv-2-4-9-on-mac-osx-with-python-support/) for install opencv with Homebrew. For me, this boiled down to:

```bash
brew tap homebrew/science
brew install opencv
sudo ln -s /usr/local/Cellar/opencv/2.4.9/lib/python2.7/site-packages/cv.py /Library/Python/2.7/site-packages/cv.py
sudo ln -s /usr/local/Cellar/opencv/2.4.9/lib/python2.7/site-packages/cv2.so /Library/Python/2.7/site-packages/cv2.so
```

## Usage

A typical usage looks like this:

```python
from gopro import GoPro
camera = GoPro(password='password')
camera.command('record', 'on')
status = camera.status()
```

## API

* `GoPro(password, ip='10.5.5.9')` - initialize a camera object
* `password(password)` - get or set the password of a camera object
* `status()` - get status packets and translate them
* `image()` - get an image and return it as a base64-encoded PNG string
* `command(param, value)` - send one of the supported commands
  * check the source for available commands - better documented list to come
* `test(url)` - a simple testing interface to try out HTTP requests
* `@classmethod config()` - returns a dictionary with the current configuration

The `image()` function is currently disabled because of difficulties installing OpenCV across platforms and because the OpenCV network functions seg fault when the wifi link is spotty.

## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.2.0 - 2014/11/24

* Renamed library from `GoProController` to `gopro`
* Added support for HERO3+ and HERO4 cameras
* Now passes Flake8
* Added testing with Travis CI
* Refactored API - the names of most methods changed but the core functionality of the library remains the same

### v0.1.1 - 2014/02/17

* Added better documentation

### v0.1.0 - 2013/10/30

* Initial release

## Todo List

* Add to PyPI
* method to list photos and videos
* method to download photos and videos
* still some information in the status byte streams i haven't translated... I don't really need the rest though
* openCV functions can get a segfault if the wifi connection is spotty - that sucks

## Contributions

Pull requests to the `develop` branch are welcomed!
