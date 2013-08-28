#!/usr/bin/python

# GoProController.py
# Josh Villbrandt <josh@javconcepts.com>
# 8/24/2013
# Based off of work by Blair Gagnon
# ugly wifi code by ZalewaPL: http://stackoverflow.com/questions/15005240/
#    connecting-to-a-protected-wifi-from-python-on-linux

# Usage:
# from GoProController import GoProController
# c = GoProController()
# c.test()

import dbus
import time
from urllib2 import *
from inspect import isfunction

class GoProController:
    def _hexToDec(val):
        return int(val, 16)
    statusURL = "http://10.5.5.9/CMD?t=PWD"
    commandURL = "http://10.5.5.9/CMD?t=PWD&p=%VAL"
    statusMatrix = {
        "bacpac/se": {
            "power": {
                "a": 18,
                "b": 20,
                "translate": {
                    "00": "off",
                    "01": "on"
                }
            }
        },
        "camera/se": {
            "batt1": {
                "a": 38,
                "b": 40,
                "translate": _hexToDec
            }
        },
        "camera/sx": { # the first 62 bytes of sx are almost the same as se
            "mode": {
                "a": 2,
                "b": 4,
                "translate": {
                    "00": "video",
                    "01": "still",
                    "02": "burst",
                    "03": "timer",
                    "07": "settings"
                }
            },
            "fov": {
                "a": 14,
                "b": 16,
                "translate": {
                    "00": "170",
                    "01": "127",
                    "02": "90"
                }
            },
            "picres": {
                "a": 17,
                "b": 18,
                "translate": {
                    "3": "5MP med",
                    "6": "7MP med",
                    "4": "7MP wide",
                    "5": "12MP wide"
                }
            },
            "secselapsed": {
                "a": 26,
                "b": 30,
                "translate": _hexToDec
            },
            "orientation": {
                "a": 37,
                "b": 38,
                "translate": {
                    "0": "up",
                    "4": "down"
                }
            },
            "charging": {
                "a": 39,
                "b": 40,
                "translate": {
                    "3": "no",
                    "4": "yes"
                }
            },
            "mem": { # i really have no idea what this is
                "a": 42,
                "b": 46,
                "translate": _hexToDec
            },
            "npics": {
                "a": 46,
                "b": 50,
                "translate": _hexToDec
            },
            "minsremaining": {
                "a": 50,
                "b": 54,
                "translate": _hexToDec
            },
            "nvids": {
                "a": 54,
                "b": 58,
                "translate": _hexToDec
            },
            "record": {
                "a": 60,
                "b": 62,
                "translate": {
                    "05": "on",
                    "04": "off"
                }
            },
            "batt2": {
                "a": 90,
                "b": 92,
                "translate": _hexToDec
            },
            "vidres": {
                "a": 100,
                "b": 102,
                "translate": {
                    "00": "WVGA",
                    "01": "720p",
                    "02": "960p",
                    "03": "1080p",
                    "04": "1440p",
                    "05": "2.7K",
                    "06": "2.7KCin",
                    "07": "4K",
                    "08": "4KCin"
                }
            },
            "fps": {
                "a": 102,
                "b": 104,
                "translate": {
                    "00": "12",
                    "01": "15",
                    "02": "24",
                    "03": "25",
                    "04": "30",
                    "05": "48",
                    "06": "50",
                    "07": "60",
                    "08": "100",
                    "09": "120",
                    "10": "240"
                }
            }
        }
    }
    commandMaxtrix = {
        "power_off": {
            "cmd": "camera/PW",
            "val": "00",
            "timeout": 0.1
        },
        "power_on": {
            "cmd": "bacpac/PW",
            "val": "01",
            "timeout": 2.0
        },
        "record_off": {
            "cmd": "camera/SH",
            "val": "00",
            "timeout": 0.1
        },
        "record_on": {
            "cmd": "camera/SH",
            "val": "01",
            "timeout": 0.1
        },
        "mode_video": {
            "cmd": "camera/CM",
            "val": "00",
            "timeout": 0.1
        }
    }
    statusTemplate = {
        "summary": "notfound", # one of "notfound", "off", "on", or "recording"
        "raw": {}
    }
    currentSSID = None
    bus = None
    manager = None
    device_path = None
    device = None
    networkTimeout = 15 # seconds
    
    def __init__(self, device_name = "ra0"):
        self.bus = dbus.SystemBus()
        #Obtain handles to manager objects.
        manager_bus_object = self.bus.get_object("org.freedesktop.NetworkManager",
             "/org/freedesktop/NetworkManager")
        self.manager = dbus.Interface(manager_bus_object, "org.freedesktop.NetworkManager")
        # Get path to the 'wlan0' device. If you're uncertain whether your WiFi
        # device is wlan0 or something else, you may utilize manager.GetDevices()
        # method to obtain a list of all devices, and then iterate over these
        # devices to check if DeviceType property equals NM_DEVICE_TYPE_WIFI (2).
        self.device_path = self.manager.GetDeviceByIpIface(device_name)
        # Connect to the device's Wireless interface and obtain list of access
        # points.
        self.device = dbus.Interface(self.bus.get_object("org.freedesktop.NetworkManager",
            self.device_path), "org.freedesktop.NetworkManager.Device.Wireless")
        
        # enable wifi if it isn't already
        manager_props = dbus.Interface(manager_bus_object, "org.freedesktop.DBus.Properties")
        wifi_enabled = manager_props.Get("org.freedesktop.NetworkManager", "WirelessEnabled")
        if not wifi_enabled:
            #print "Enabling WiFi and sleeping for 10 seconds ..."
            manager_props.Set("org.freedesktop.NetworkManager", "WirelessEnabled", True)
            # Give the WiFi adapter some time to scan for APs. This is absolutely
            # the wrong way to do it, and the program should listen for
            # AccessPointAdded() signals, but it will do.
            time.sleep(10)
    
    def connect(self, ssid, password):
        # skip the connect process if we are already on this network
        if ssid == self.currentSSID:
            # TODO: do a more comprehensive check - this could have changed and we don't know about it
            return True
        else:
            try:
                # not to self: a new camera won't be seen for at least 10 seconds
                
                # Identify our access point. We do this by comparing our desired SSID
                # to the SSID reported by the AP.
                ap_list = self.device.GetAccessPoints()
                ap_path = None
                for path in ap_list:
                    ap_props = dbus.Interface(self.bus.get_object("org.freedesktop.NetworkManager", path),
                        "org.freedesktop.DBus.Properties")
                    ap_ssid = ap_props.Get("org.freedesktop.NetworkManager.AccessPoint", "Ssid")
                    
                    # Returned SSID is a list of ASCII values. Let's convert it to a proper
                    # string.
                    ap_ssid_str = "".join(chr(i) for i in ap_ssid)
                    if ap_ssid_str == ssid:
                        ap_path = path
                        break
                
                # attempt a connection
                if ap_path:
                    # At this point we have all the data we need. Let's prepare our connection
                    # parameters so that we can tell the NetworkManager what is the passphrase.
                    connection_params = {
                        "802-11-wireless": {
                            "security": "802-11-wireless-security",
                        },
                        "802-11-wireless-security": {
                            "key-mgmt": "wpa-psk",
                            "psk": password
                        },
                    }
        
                    # Establish the connection.
                    self.currentSSID = None
                    settings_path, connection_path = self.manager.AddAndActivateConnection(
                        connection_params, self.device_path, ap_path)
                    # unfortunately this adds a new "connection" every time! lame...
                    # would like to prevent "auto connect" so that it doesn't prompt me when the camera is not there
                    #print "settings_path =", settings_path
                    #print "connection_path =", connection_path
                
                    # Wait until connection is established. This may take a few seconds.
                    #print """Waiting for connection to reach """ \"""NM_ACTIVE_CONNECTION_STATE_ACTIVATED state ..."""
                    connection_props = dbus.Interface(
                        self.bus.get_object("org.freedesktop.NetworkManager", connection_path),
                        "org.freedesktop.DBus.Properties")
                    start = time.time()
                    while time.time()-start < self.networkTimeout:
                        # Loop forever until desired state is detected.
                        #
                        # A timeout should be implemented here, otherwise the program will
                        # get stuck if connection fails.
                        #
                        # IF PASSWORD IS BAD, NETWORK MANAGER WILL DISPLAY A QUERY DIALOG!
                        # This is something that should be avoided, but I don't know how, yet.
                        #
                        # Also, if connection is disconnected at this point, the Get()
                        # method will raise an org.freedesktop.DBus.Error.UnknownMethod
                        # exception. This should also be anticipated.
                        state = connection_props.Get(
                            "org.freedesktop.NetworkManager.Connection.Active", "State")
                        if state == 2: #NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                            # Connection established!
                            self.currentSSID = ssid
                            return True
                        time.sleep(0.01)
            except:
                pass
        
        # catchll return
        return False
    
    def getStatus(self, ssid, password):
        status = self.statusTemplate.copy()
        camActive = True
        
        # attempt to connect to the correct camera
        if not self.connect(ssid, password):
            camActive = False
        
        # loop through different status URLs
        for cmd in self.statusMatrix:
            
            # stop sending requests if a previous request failed
            if camActive:
                url = self.statusURL.replace("CMD", cmd).replace("PWD", password)
                
                # attempt to contact the camera
                try:
                    response = urlopen(url, timeout=1).read().encode("hex")
                    status['raw'][cmd] = response # save raw response
                    
                    # loop through different parts that we know how to translate
                    for item in self.statusMatrix[cmd]:
                        args = self.statusMatrix[cmd][item]
                        part = response[args["a"]:args["b"]]
                        
                        # translate the response value if we know how
                        if "translate" in args:
                            if isfunction(args["translate"]):
                                status[item] = args["translate"](part)
                            elif part in args["translate"]:
                                status[item] = args["translate"][part]
                            else:
                                status[item] = "translate error (" + part + ")"
                        else:
                            status[item] = part
                except:
                    camActive = False
        
        # build summary
        if "record" in status and status["record"] == "on":
            status["summary"] = "recording"
        elif "power" in status and status["power"] == "on":
            status["summary"] = "on"
        elif "power" in status and status["power"] == "off":
            status["summary"] = "off"
        
        return status
    
    def sendCommand(self, ssid, password, command):
        if self.connect(ssid, password):
            if command in self.commandMaxtrix:
                args = self.commandMaxtrix[command]
                url = self.commandURL.replace("CMD", args["cmd"]).replace("PWD",
                    password).replace("VAL", args["val"])
                
                # attempt to contact the camera
                try:
                    response = urlopen(url, timeout=args["timeout"]).read()
                    return True
                except HTTPError, e:
                    print "    HTTPError opening " + url + ": " + str(e.code)
                except URLError, e:
                    print "    URLError opening " + url + ": "
                    print e.args
                
        # catchall return statement
        return False
    
    def test(self):
        print self.getStatus("cam1", "password")
