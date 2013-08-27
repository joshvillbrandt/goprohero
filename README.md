GoProController
===============

A lightweight Python class for interfacing with multiple GoPros.

This class can interfaces with GoPro cameras in their wifi ad-hoc mode (aka GoPro App mode.) When used with multiple cameras, the class will automatically jump between networks.

# Todo

* hack the infrastructure network that the GoPro Remote makes and learn how to have GoPros on only one network
* look into the wifi_networks list that in the settings.in file that is present when updating GoPro firmware
* revamp crappy wifi connect code
* respond better to keyboard interrupts
