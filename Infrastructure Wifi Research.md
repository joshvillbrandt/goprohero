
# Setup

This follow setup allows a linux computer to appear as a GoPro remote to the GoPro cameras. To do this, we will set up an access point and DHCP server. In order to appear as a GoPro remote, the MAC address of the access point interface must use GoPro's OUI which is D8:96:85. So something like D8:96:85:00:00:00 will do. The access point SSID also must be in a special form - "HERO-RC-#####" where the hashes are the last 6 characters of the AP's mac address. From there, we use DHCP to hand the camera an IP, and then it is on our network!

I used http://www.cyberciti.biz/faq/debian-ubuntu-linux-setting-wireless-access-point/ and http://ubuntuforums.org/showthread.php?t=1488953 to help me develop some of these snippits.

## Wifi adapter

You'll need a wifi adapter that can support master mode to set up an access point. I'm using a ALFA USB WiFi AWUS036NHA with the well-supported Atheros AR9271 chipset.

On that is installed, we need to change its mac address to one from the GoPro's OUI (D8:96:85) so that the cameras will recognize it. We can do that like so:

    sudo ifconfig wlan0 down
    sudo ifconfig wlan0 hw ether D8:96:85:00:00:00 # was originally 00:c0:ca:71:ca:4f
    sudo ifconfig wlan0 up
    ifconfig

## Set up access point

Install the host AP deamon like so:

    sudo apt-get install hostapd

Edit '/etc/default/hostapd' to point to a hostapd config file by setting the DAEMON_CONF variable:

    DAEMON_CONF="/etc/hostapd/hostapd.conf"

Then set up the hostapd config file! It should look something like this:

    interface=wlan0
    driver=nl80211
    country_code=US
    ssid=HERO-RC-000000
    hw_mode=b
    channel=6

Start the server using:

    sudo service hostapd start

## Set up DHCP server

This portion is optional if you decide to bridge your access point network with an already-established LAN. Find details on bridging networking interfaces on the web.

    sudo apt-get install dhcp3-server

Tell the DHCP server to service our wireless interface by editing '/etc/default/isc-dhcp-server':

   INTERFACES="wlan0"

Set up the DHCP config file '/etc/dhcp/dhcpd.conf'. Mine looks like this:

    default-lease-time 86400;
    max-lease-time 86400;
    option subnet-mask 255.255.255.0;
    option broadcast-address 192.168.1.255;
    option routers 192.168.1.254;
    option domain-name-servers 192.168.1.1, 192.168.1.2;
    option domain-name "mydomain.example";
    
    subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.10 192.168.1.200;
    }

You can that start the DHCP server:

    sudo service isc-dhcp-server start

## Install Scapy

    sudo apt-get install python-scapy

# Usage

    sudo python remote.py









sudo ifconfig wlan0 192.168.0.254 netmask 255.255.255.0

log-facility local7;
ddns-update-style none;
default-lease-time 43200;
max-lease-time 86400;

subnet 192.168.0.0 netmask 255.255.255.0 {
  interface wlan0;
  range 192.168.0.10 192.168.0.20;
  option subnet-mask 255.255.255.0;
  option broadcast-address 192.168.0.255;
}
