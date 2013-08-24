#!/usr/bin/python

# GoPro Hero3 Controller
# Blair Gagnon
# 8/22/2013
# originally based off of: http://ubuntuone.com/5G2W2LtiQEsXW75uxu2dPl

import dbus
import time
from urllib2 import *
import scipy as sp
import cv2
import time

####################### Global Variables: Don't judge, I know this is messy!
# list of GoPro SSIDs
ssids =["GoPro3_01", "GoPro3_02"]

# same password for every camera and an easy password at that
password = "password"

################################ wifi setup: this code is from internet. See Wifi definitions at bottom of file
bus = dbus.SystemBus()
#Obtain handles to manager objects.
manager_bus_object = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
manager = dbus.Interface(manager_bus_object, "org.freedesktop.NetworkManager")
manager_props = dbus.Interface(manager_bus_object, "org.freedesktop.DBus.Properties")
# Get path to the 'wlan0' device. If you're uncertain whether your WiFi
# device is wlan0 or something else, you may utilize manager.GetDevices()
# method to obtain a list of all devices, and then iterate over these
# devices to check if DeviceType property equals NM_DEVICE_TYPE_WIFI (2).
device_path = manager.GetDeviceByIpIface("wlan0")
# Connect to the device's Wireless interface and obtain list of access
# points.
device = dbus.Interface(bus.get_object("org.freedesktop.NetworkManager", device_path), "org.freedesktop.NetworkManager.Device.Wireless")
connection_path=""
settings_path=""
was_wifi_enabled = False
####################################################################################################################




####################### Used for sending commands
#Standard http url set up code, with a special if statement for turning off the cameras.
#Usually ends up sending a urlopen request to the already shutoff camera so this sort of ignores that.
def sendCommand(device, group, action, timeout):
    try:
        url = "http://10.5.5.9/"+device+"/"+group+"?t="+password+"&p=%"+action
        response=urlopen(url, None, timeout)
    except:
        if (group == "PW" and action == "00"):
            print("A Power Off command received no response.")
        else:
            print("Error Sending Command")


###################### Turns the current camera on
def powerOn():
    sendCommand("bacpac", "PW", "01", 2.0)
    

###################### Turns the current camera off
def powerOff():
    sendCommand("camera", "PW", "00", 0.1)
    

###################### Starts the current camera recording
def startRecord():
    sendCommand("camera", "SH", "01", 0.1)


###################### Stops the current camera recording
def stopRecord():
    sendCommand("camera", "SH", "00", 0.1)


###################### Set camera to video mode
def modeVideo():
    sendCommand("camera", "CM", "00", 0.1)
    

###################### Gets the power status of the current camera
# The power status is found in the last hex number of the response message to this url.
def getPowerStatus():
    powerStatus = "fail"
    try:
        powerStatus=urlopen("http://10.5.5.9/bacpac/se?t=password", timeout=1).read().encode("hex")[30:32]
    except URLError:
        pass
    return powerStatus


###################### Gets the setting status of the current camera
# returns the stringafied version of the response message for further processing
def getSettingStatus():
    settingStatus = "fail"
    try:
        settingStatus=urlopen("http://10.5.5.9/camera/sx?t=password", timeout=1).read().encode("hex")
    except:
        pass
    return settingStatus


##################### Gets battery percentage
#battery percentage is only found here. It seems to be very accurate and the battery dies ~1-2 after
#reaching 0%
#returns the stringified hex version of the battery percentage (represents % of full battery.)
def getBatteryPercentage():
    batteryPercentage = "fail"
    try:
        batteryPercentage = urlopen("http://10.5.5.9/camera/se?t=password", timeout=1).read().encode("hex")[38:40]
    except:
        pass
    return batteryPercentage


###################### Trigger all cameras on
def triggerAllOn():
    totalPrevious = time.time()
    global ssids
    global passwords
    for cam in ssids:
        previous = time.time()
        connectWifi(cam, password)
        while (getPowerStatus() != '01'):
            powerOn()
            time.sleep(1)
        disconnectWifi()
        print(cam+": Powered On")
        print("Cyle Time: "+str(time.time()-previous)+"\n")
    print("Total Cycle Time: "+str(time.time()-totalPrevious))
    

###################### Trigger all cameras off
def triggerAllOff():
    totalPrevious = time.time()
    global ssids
    global passwords
    for cam in ssids:
        previous = time.time()
        connectWifi(cam, password)
        while (getPowerStatus() != '00'):
            powerOff()
            time.sleep(1)
        disconnectWifi()
        print(cam+": Powered Off")
        print("Cyle Time: "+str(time.time()-previous)+"\n")
    print("Total Cycle Time: "+str(time.time()-totalPrevious))


###################### Trigger all cameras record
def triggerAllRecordOn():
    totalPrevious = time.time()
    global ssids
    global passwords
    for cam in ssids:
        previous = time.time()
        connectWifi(cam, password)
        while (getSettingStatus()[2:4]!="00"):
            modeVideo()
            time.sleep(1)
        while (getSettingStatus()[60:62]!="05"):
            startRecord()
            time.sleep(1)
        disconnectWifi()
        print(cam+": Recording")
        print("Cyle Time: "+str(time.time()-previous)+"\n")
    print("Total Cycle Time: "+str(time.time()-totalPrevious))



###################### Trigger all cameras record
def triggerAllRecordOff():
    totalPrevious = time.time()
    global ssids
    global passwords
    for cam in ssids:
        previous = time.time()
        connectWifi(cam, password)
        while (getSettingStatus()[60:62]!="04"):
            stopRecord()
            time.sleep(1)
        disconnectWifi()
        print(cam+": Stopped Recording")
        print("Cyle Time: "+str(time.time()-previous)+"\n")
    print("Total Cycle Time: "+str(time.time()-totalPrevious))


###################### Gets the status of all GoPro cameras
# displays the status of the cameras including the current mode, recording status, video resolution
# video FPS, video FOV and battery percentage of full charge
# the locations and values of the corresponding hex numbers were determined by changing desired settings
# and observing changes in status message content.
def displayAllStatus():
    totalPrevious = time.time()
    statusMessages=[]
    global ssids
    global password
    for cam in ssids:
        previous = time.time()
        connectWifi(cam, password)
        if (getPowerStatus() == '00'):
            statusMessages.append("Powered Off")
        else:
            tempStatus = getSettingStatus()
            tempMessage="Powered On\n"
            
            ##### Mode Determination ####            
            if (tempStatus[2:4]=="00"):
                tempMessage=tempMessage+"Mode: Video\n"
            elif (tempStatus[2:4]=="01"):
                tempMessage=tempMessage+"Mode: Camera\n"
            elif (tempStatus[2:4]=="02"):
                tempMessage=tempMessage+"Mode: Burst\n"
            elif (tempStatus[2:4]=="03"):
                tempMessage=tempMessage+"Mode: Timer\n"
            elif (tempStatus[2:4]=="07"):
                tempMessage=tempMessage+"Mode: Settings\n"
            else:
                tempMessage=tempMessage+"Mode: Error\n"
                
            #### Recording Status Determination ####
            if (tempStatus[60:62]=="04"):
                tempMessage=tempMessage+"Recording: No\n"
            elif (tempStatus[60:62]=="05"):
                tempMessage=tempMessage+"Recording: Yes\n"
            else:
                tempMessage=tempMessage+"Recording: Error\n"
                
            #### Resolution Determination ####
            if (tempStatus[100:102]=="01"):
                tempMessage=tempMessage+"Resolution: 720\n"
            elif (tempStatus[100:102]=="02"):
                tempMessage=tempMessage+"Resolution: 960\n"
            elif (tempStatus[100:102]=="03"):
                tempMessage=tempMessage+"Resolution: 1080\n"
            else:
                tempMessage=tempMessage+"Resolution: Error\n"
                
            #### Frames Per Second Determination ####
            if (tempStatus[102:104]=="02"):
                tempMessage=tempMessage+"FPS: 24\n"
            elif (tempStatus[102:104]=="04"):
                tempMessage=tempMessage+"FPS: 30\n"
            elif (tempStatus[102:104]=="05"):
                tempMessage=tempMessage+"FPS: 48\n"
            elif (tempStatus[102:104]=="07"):
                tempMessage=tempMessage+"FPS: 60\n"
            elif (tempStatus[102:104]=="08"):
                tempMessage=tempMessage+"FPS: 100\n"
            elif (tempStatus[102:104]=="09"):
                tempMessage=tempMessage+"FPS: 120\n"
            else:
                tempMessage=tempMessage+"FPS: Error\n"

            #### Feild of View Determination ####
            if (tempStatus[14:16]=="00"):
                tempMessage=tempMessage+"FOV: Wide\n"
            elif (tempStatus[14:16]=="01"):
                tempMessage=tempMessage+"FOV: Medium\n"
            elif (tempStatus[14:16]=="02"):
                tempMessage=tempMessage+"FOV: Narrow\n"
            else:
                tempMessage=tempMessage+"FOV: Error\n"

            #### Battery Percentage Determination ####
            tempMessage=tempMessage+"Battery Percentage: "+str(int(getBatteryPercentage(), 16))+"%"
                       
            statusMessages.append(tempMessage)            
        disconnectWifi()
        print(cam+": "+statusMessages[len(statusMessages)-1])
        print("Cyle Time: "+str(time.time()-previous)+"\n")
    print("Total Cycle Time: "+str(time.time()-totalPrevious))










###########################################################################################################################
###########################################################################################################################
#######                                        Found on Internet: Beware!                                               ###
#######           http://stackoverflow.com/questions/15005240/connecting-to-a-protected-wifi-from-python-on-linux       ###
###########################################################################################################################
###########################################################################################################################    

###################### Connects to a WPA protected WIFI network
def connectWifi(ssid, passphrase):
    global connection_path
    global settings_path
    global was_wifi_enabled
    global device_path
    # Enable Wireless. If Wireless is already enabled, this does nothing.
    was_wifi_enabled = manager_props.Get("org.freedesktop.NetworkManager",
                                         "WirelessEnabled")
    if not was_wifi_enabled:
        #print "Enabling WiFi and sleeping for 10 seconds ..."
        manager_props.Set("org.freedesktop.NetworkManager", "WirelessEnabled",
                          True)
        # Give the WiFi adapter some time to scan for APs. This is absolutely
        # the wrong way to do it, and the program should listen for
        # AccessPointAdded() signals, but it will do.
        time.sleep(10)
        
    accesspoints_paths_list = device.GetAccessPoints()

    # Identify our access point. We do this by comparing our desired SSID
    # to the SSID reported by the AP.
    our_ap_path = None
    for ap_path in accesspoints_paths_list:
        ap_props = dbus.Interface(
            bus.get_object("org.freedesktop.NetworkManager", ap_path),
            "org.freedesktop.DBus.Properties")
        ap_ssid = ap_props.Get("org.freedesktop.NetworkManager.AccessPoint",
                               "Ssid")
        # Returned SSID is a list of ASCII values. Let's convert it to a proper
        # string.
        str_ap_ssid = "".join(chr(i) for i in ap_ssid)
        #print ap_path, ": SSID =", str_ap_ssid
        if str_ap_ssid == ssid:
            our_ap_path = ap_path
            break

    if not our_ap_path:
        "AP not found :("
        pass
    #print "Our AP: ", our_ap_path

    # At this point we have all the data we need. Let's prepare our connection
    # parameters so that we can tell the NetworkManager what is the passphrase.
    connection_params = {
        "802-11-wireless": {
            "security": "802-11-wireless-security",
        },
        "802-11-wireless-security": {
            "key-mgmt": "wpa-psk",
            "psk": passphrase
        },
    }

    # Establish the connection.
    settings_path, connection_path = manager.AddAndActivateConnection(
        connection_params, device_path, our_ap_path)
    #print "settings_path =", settings_path
    #print "connection_path =", connection_path

    # Wait until connection is established. This may take a few seconds.
    NM_ACTIVE_CONNECTION_STATE_ACTIVATED = 2
    #print """Waiting for connection to reach """ \"""NM_ACTIVE_CONNECTION_STATE_ACTIVATED state ..."""
    connection_props = dbus.Interface(
        bus.get_object("org.freedesktop.NetworkManager", connection_path),
        "org.freedesktop.DBus.Properties")
    state = 0
    while True:
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
        if state == NM_ACTIVE_CONNECTION_STATE_ACTIVATED:
            break
        time.sleep(0.001)
    #print "Connection established!"


##################### Disconnects from the current Wifi connection
def disconnectWifi():
    global connection_path
    global settings_path
    global was_wifi_enabled
    #print "Disconnecting ..."

    # Clean up: disconnect and delete connection settings. If program crashes
    # before this point is reached then connection settings will be stored
    # forever.
    # Some pre-init cleanup feature should be devised to deal with this problem,
    # but this is an issue for another topic.
    manager.DeactivateConnection(connection_path)
    settings = dbus.Interface(
        bus.get_object("org.freedesktop.NetworkManager", settings_path),
        "org.freedesktop.NetworkManager.Settings.Connection")
    settings.Delete()

    # Disable Wireless (optional step)
    if not was_wifi_enabled:
        manager_props.Set("org.freedesktop.NetworkManager", "WirelessEnabled",
                          False)
   #print "DONE!"

    