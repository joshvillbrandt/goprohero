# Setup

Install the `goprohero` library:

```bash
sudo pip install goprohero
```

To connect with a GoPro, you will need to have the camera on the local network. This can be accomplished by:

1. Turning on the GoPro wireless "app" mode - this instructs the camera to create an AdHoc wireless network
1. Connecting the computer running this library to the camera's network

This connection process can be automated with the [GoProController](https://github.com/joshvillbrandt/GoProController) or with the included command line interface.

## Live Stream Image Capture

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

Note that having the camera's `preview` setting set to `on` might be required for the live stream image capture.
