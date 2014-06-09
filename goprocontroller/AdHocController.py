#!/usr/bin/python

# GoProController.py
# Josh Villbrandt <josh@javconcepts.com>, Blair Gagnon <blairgagnon@gmail.com>
# 8/24/2013

# Reference URLs:
# http://projects.gnome.org/NetworkManager/developers/
# http://projects.gnome.org/NetworkManager/developers/settings-spec-08.html
# ugly wifi code by ZalewaPL: http://stackoverflow.com/questions/15005240/
# more commands here: http://ubuntuone.com/5G2W2LtiQEsXW75uxu2dPl

from .GoPro import GoPro
import dbus
import time
import logging
import copy


class AdHocController:
    camera = None
    currentSSID = None
    bus = None
    manager = None
    device_path = None
    device = None
    networkTimeout = 15  # seconds
    connection_path = None
    settings_path = None

    def __init__(
            self,
            device_name='ra0',
            log_file='controller.log',
            log_level=logging.INFO,
            log_format='%(levelname)-7s %(asctime)s   %(message)s'):

        # usage one GoPro instaces for all cameras
        self.camera = GoPro()

        # setup log
        logging.basicConfig(
            filename=log_file, format=log_format, level=log_level)
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger('').addHandler(console)

        # set up wifi
        self.bus = dbus.SystemBus()
        #Obtain handles to manager objects.
        manager_bus_object = self.bus.get_object(
            'org.freedesktop.NetworkManager',
            '/org/freedesktop/NetworkManager')
        self.manager = dbus.Interface(
            manager_bus_object, 'org.freedesktop.NetworkManager')
        # Get path to the 'wlan0' device. If you're uncertain whether your WiFi
        # device is wlan0 or something else, you may utilize manager.GetDevices()
        # method to obtain a list of all devices, and then iterate over these
        # devices to check if DeviceType property equals NM_DEVICE_TYPE_WIFI (2).
        self.device_path = self.manager.GetDeviceByIpIface(device_name)
        # Connect to the device's Wireless interface and obtain list of access
        # points.
        self.device = dbus.Interface(
            self.bus.get_object(
                'org.freedesktop.NetworkManager', self.device_path),
            'org.freedesktop.NetworkManager.Device.Wireless')

        # enable wifi if it isn't already
        manager_props = dbus.Interface(
            manager_bus_object, 'org.freedesktop.DBus.Properties')
        wifi_enabled = manager_props.Get(
            'org.freedesktop.NetworkManager', 'WirelessEnabled')
        if not wifi_enabled:
            #print 'Enabling WiFi and sleeping for 10 seconds ...'
            manager_props.Set(
                'org.freedesktop.NetworkManager', 'WirelessEnabled', True)
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
            logging.info('connect(%s) - attempting connection', ssid)
            try:
                # disconnect from previous connection
                try:
                    # we might be switching connections even if connection_path is not None
                    if self.connection_path is not None:
                        self.manager.DeactivateConnection(self.connection_path)
                        settings = dbus.Interface(
                            self.bus.get_object(
                                'org.freedesktop.NetworkManager',
                                self.settings_path),
                            'org.freedesktop.NetworkManager.Settings.Connection')
                        settings.Delete()
                except:
                    pass

                # note to self: a new camera won't be seen for at least 10 seconds

                # Identify our access point. We do this by comparing our desired SSID
                # to the SSID reported by the AP.
                ap_list = self.device.GetAccessPoints()
                ap_path = None
                for path in ap_list:
                    ap_props = dbus.Interface(
                        self.bus.get_object(
                            'org.freedesktop.NetworkManager', path),
                        'org.freedesktop.DBus.Properties')
                    ap_ssid = ap_props.Get(
                        'org.freedesktop.NetworkManager.AccessPoint', 'Ssid')

                    # Returned SSID is a list of ASCII values. Let's convert it to a proper
                    # string.
                    ap_ssid_str = ''.join(chr(i) for i in ap_ssid)
                    if ap_ssid_str == ssid:
                        ap_path = path
                        break

                # attempt a connection
                if ap_path:
                    # At this point we have all the data we need. Let's prepare our connection
                    # parameters so that we can tell the NetworkManager what is the passphrase.
                    connection_params = {
                        '802-11-wireless': {
                            'security': '802-11-wireless-security',
                        },
                        '802-11-wireless-security': {
                            'key-mgmt': 'wpa-psk',
                            'psk': password
                        },
                    }

                    # Establish the connection.
                    self.currentSSID = None
                    self.settings_path, self.connection_path = self.manager.AddAndActivateConnection(
                        connection_params, self.device_path, ap_path)
                    # unfortunately this adds a new 'connection' every time! lame...
                    # would like to prevent 'auto connect' so that it doesn't prompt me when the camera is not there
                    #print 'settings_path =', settings_path
                    #print 'connection_path =', connection_path

                    # Wait until connection is established. This may take a few seconds.
                    #print '''Waiting for connection to reach ''' \'''NM_ACTIVE_CONNECTION_STATE_ACTIVATED state ...'''
                    connection_props = dbus.Interface(
                        self.bus.get_object(
                            'org.freedesktop.NetworkManager',
                            self.connection_path),
                        'org.freedesktop.DBus.Properties')
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
                            'org.freedesktop.NetworkManager.Connection.Active',
                            'State')
                        if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                            # Connection established!
                            self.currentSSID = ssid
                            logging.info(
                                'connect(%s) - connection success', ssid)
                            return True
                        time.sleep(0.01)
            except Exception as e:
                logging.warning(
                    'connect(%s) - connection failure %s %s',
                    ssid, type(e), e.args)

        # catchll return
        logging.warning('connect(%s) - connection failure', ssid)
        return False

    def getStatus(self, ssid, password):
        if self.connect(ssid, password):
            self.camera.setPassword(password)
            return self.camera.getStatus()
        else:
            return copy.deepcopy(GoPro.statusTemplate)

    def getImage(self, ssid, password):
        if self.connect(ssid, password):
            self.camera.setPassword(password)
            return self.camera.getImage()
        else:
            return False

    def sendCommand(self, ssid, password, command):
        if self.connect(ssid, password):
            self.camera.setPassword(password)
            return self.camera.sendCommand(command)
        else:
            return False
