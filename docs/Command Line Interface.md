# Command Line Interface

A command line interface for controlling GoPro cameras is also made available. This interface utilizes the [wireless](https://github.com/joshvillbrandt/wireless) library to automatically jump between networks.

```bash
usage: goproctl [-h] ssid [ssid ...] password param value

A command line interface for passing commands to one or more GoPros.

positional arguments:
  ssid        ssid of the gopro to control
  password    the password for the gopro(s)
  param       the parameter to be changed
  value       the value to set the parameter to

optional arguments:
  -h, --help  show this help message and exit
```

For example, try:

```bash
goproctl gopro3-0 password power on
```

Other common commands are `power sleep`, `record on`, and `record off`.
