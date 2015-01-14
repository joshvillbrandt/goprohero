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
picres | `5MP wide`, `5MP med`, `7MP med`, `7MP wide`, `8MP med`, `11MP wide`, `12MP wide`
vidres | `WVGA`, `720p`, `960p`, `1080p`, `1440p`, `2.7K`, `2.7K 17:9 Cinema`, `4K`, `4K 17:9 Cinema`, `1080p SuperView`, `720p SuperView`
fov | `170`, `127`, `90`
fps | `12`, `12.5`, `15`, `24`, `25`, `30`, `48`, `50`, `60`, `100`, `120`, `240`
looping | `off`, `5 minutes`, `20 minutes`, `60 minutes`, `120 minutes`, `max`
protune | `off`, `on`
delete_last | n/a
delete_all | n/a

## Status

The following status parameters are interpreted from the GoPro status endpoints: `power`, `batt1`, `batt2`, `mode`, `defaultmode`, `spotmeter`, `autooff`, `fov`, `picres`, `minselapsed`, `secselapsed`, `orientation`, `charging`, `picsremaining`, `npics`, `minsremaining`, `nvids`, `record`, `vidres`, `fps`, `lowlight`, `looping`, `attachment`, `name`, `model`, and `firmware`. View the source file for a complete list of possible values for each status parameter.
