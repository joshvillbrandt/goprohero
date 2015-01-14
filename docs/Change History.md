# Change History

This project uses [semantic versioning](http://semver.org/).

## v0.2.6 - future

* TODO: Made arguments to `goproctl` keyword arguments and added the `interface` argument
* Fixed commanding for commands without values like `delete_all` and `delete_last`
* Added `defaultmode`, `minselapsed`, `spotmeter`, `autooff`, `lowlight`, `looping`, and `attachment` parameters
* Fixed erroneous `secselapsed` and `record` parameter
* Renamed `mem` parameter to `picsremaining`
* Added a list of supported status parameters to the docs API page
* Added GoPro firmware upgrade instructions to the docs

## v0.2.5 - 2014/12/01

* Fixed bug that prevent `goproctl` from working

## v0.2.4 - 2014/12/01

* Removed dependency on `pandoc`
* Added publishing instructions

## v0.2.3 - 2014/11/27

* `goproctl` uses the existing network connection if possible
* `goproctl` can now get the status of cameras

## v0.2.2 - 2014/11/26

* Renamed library from `gopro` to `goprohero`
* Added to PyPI
* Started better documentation with readthedocss support

## v0.2.1 - 2014/11/24

* Added `goproctl` command line interface

## v0.2.0 - 2014/11/24

* Renamed library from `GoProController` to `gopro`
* Added support for HERO3+ and HERO4 cameras
* Now passes Flake8
* Added testing with Travis CI
* Refactored API - the names of most methods changed but the core functionality of the library remains the same

## v0.1.1 - 2014/02/17

* Added better documentation

## v0.1.0 - 2013/10/30

* Initial release
