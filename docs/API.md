# API

First create a camera instance:

* `camera = GoProHero([ip, password, loglevel])` - initialize a camera object

Then, the follow methods are available on the camera instance:

* `password(password)` - get or set the password of a camera object
* `command(param, value)` - send one of the supported commands
* `status()` - get status packets and translate them
* `image()` - get an image and return it as a base64-encoded PNG string
* `test(url)` - a simple testing interface to try out HTTP requests

The following class methods are also available:

* `@classmethod config()` - returns a dictionary with the current configuration

## Commands

These commands are used for both `camera.command()` and the `goproctl` command line interface.

Parameter | Values
--- |:---
power | `sleep`, `on`
record | `off`, `on`
preview | `off`, `on`
orientation | `up`, `down`
mode | `video`, `still`, `burst`, `timelapse`, `timer`, `hdmi`
volume | `0`, `70`, `100`
locate | `off`, `on`

## Status

The following status parameters are interpreted from the GoPro status endpoints: `power`, `batt1`, `batt2`, `mode`, `fov`, `picres`, `secelapsed`, `orientation`, `charging`, `mem`, `npics`, `minsremaining`, `nvids`, `record`, `vidres`, `fps`, `name`, `model`, and `firmware`. View the source file for a complete list of possible values for each status parameter.
