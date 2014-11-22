from abc import ABCMeta, abstractmethod
import subprocess


# attempt to retrieve the iwlist response for a given ssid
def cmd(cmd):
    return subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE).stdout.read()


# abstracts away the wifi details
class Wireless:
    _driver = None

    # init
    def __init__(self):
        name = self._detect()
        if name == 'nmcli':
            self._driver = NmcliWireless()
        elif name == 'networksetup':
            self._driver = NetworksetupWireless()

    def _detect(self):
        # try nmcli (Ubuntu 14.04)
        response = cmd('which nmcli')
        if len(response) > 0 and 'not found' not in response:
            return 'nmcli'

        # try networksetup (Mac OS 10.10)
        response = cmd('which networksetup')
        if len(response) > 0 and 'not found' not in response:
            return 'networksetup'

        raise Exception('Cannot find compatible wireless API.')

    # connect to a network
    def connect(self, **kwargs):
        return self._driver.connect(**kwargs)

    # returned the ssid of the current network
    def current(self, **kwargs):
        return self._driver.current(**kwargs)


# abstract class for all wireless drivers
class WirelessDriver:
    __metaclass__ = ABCMeta

    # connect to a network
    @abstractmethod
    def connect(self, ssid, password):
        pass

    # returned the ssid of the current network
    @abstractmethod
    def current(self):
        pass


# Ubuntu Driver
class NmcliWireless(WirelessDriver):
    _currentSSID = None

    # connect to a network
    def connect(self, ssid, password):
        response = cmd('nmcli dev wifi connect {} password {}'.format(
            ssid, password))

        if len(response) == 0:
            self._currentSSID = ssid
            return True
        else:
            self._currentSSID = None
            return False

    # returned the ssid of the current network
    def current(self):
        # TODO: actually check the current SSID with a shell call
        # nmcli dev wifi | grep yes
        return self._currentSSID


# OS X Driver
class NetworksetupWireless(WirelessDriver):
    _interface = None
    _currentSSID = None

    # init
    def __init__(self):
        self._interface = self._autoDetectInterface()

    def _autoDetectInterface(self):
        response = cmd('networksetup -listallhardwareports')
        lines = response.splitlines()

        # parse response
        detectedWifi = False
        for line in lines:
            if detectedWifi:
                # this line has our interface name in it
                return line.replace('Device: ', '')
            else:
                # search for the line that has 'Wi-Fi' in it
                if 'Wi-Fi' in line:
                    detectedWifi = True

        # if we are here then we failed to auto detect the interface
        raise Exception('Unabled to auto-detect the network interface.')

    # connect to a network
    def connect(self, ssid, password):
        response = cmd('networksetup -setairportnetwork {} {} {}'.format(
            self._interface, ssid, password))

        if len(response) == 0:
            self._currentSSID = ssid
            return True
        else:
            self._currentSSID = None
            return False

    # returned the ssid of the current network
    def current(self):
        # TODO: actually check the current SSID with a shell call
        return self._currentSSID
