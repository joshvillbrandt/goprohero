# API

* `GoPro(password, ip='10.5.5.9')` - initialize a camera object
* `password(password)` - get or set the password of a camera object
* `status()` - get status packets and translate them
* `image()` - get an image and return it as a base64-encoded PNG string
* `command(param, value)` - send one of the supported commands
  * check the source for available commands - better documented list to come
* `test(url)` - a simple testing interface to try out HTTP requests
* `@classmethod config()` - returns a dictionary with the current configuration

## Commands

todo
