#!/usr/bin/python

# GoProController.py
# Josh Villbrandt <josh@javconcepts.com>
# 8/24/2013
# Based off of work by Blair Gagnon

# Usage:
# from GoProController import GoProController
# c = GoProController()
# c.test()

from urllib2 import *

class GoProController:
    statusURL = 'http://10.5.5.9/CMD?t=PWD'
    commandURL = 'http://10.5.5.9/CMD?t=PWD&p=%VAL'
    statusMatrix = {
        'bacpac/se': {
            'power': {
                'a': 30,
                'b': 32,
                'translate': {
                    '00': 'off',
                    '01': 'on'
                }
            }
        },
        'camera/se': {
            'batt': {
                'a': 38,
                'b': 40
            }
        },
        'camera/sx': {
            'mode': {
                'a': 2,
                'b': 4,
                'translate': {
                    '00': 'video',
                    '01': 'still',
                    '02': 'burst',
                    '03': 'timer',
                    '07': 'settings'
                }
            },
            'record': {
                'a': 60,
                'b': 62,
                'translate': {
                    '05': 'on',
                    '04': 'off'
                }
            },
            'res': {
                'a': 100,
                'b': 102,
                'translate': {
                    '01': '720p',
                    '02': '960p',
                    '03': '1080p'
                }
            },
            'fps': {
                'a': 102,
                'b': 104,
                'translate': {
                    '00': '12',
                    '01': '15',
                    '02': '24',
                    '03': '25',
                    '04': '30',
                    '05': '48',
                    '06': '50',
                    '07': '60',
                    '08': '100',
                    '09': '120',
                    '10': '240'
                }
            },
            'fov': {
                'a': 14,
                'b': 16,
                'translate': {
                    '00': 'wide (170)',
                    '01': 'medium (127)',
                    '02': 'narrow (90)'
                }
            }
        }
    }
    commandMaxtrix = {
        'power_off': {
            'cmd': 'camera/PW',
            'val': '00',
            'timeout': 0.1
        },
        'power_on': {
            'cmd': 'bacpac/PW',
            'val': '01',
            'timeout': 2.0
        },
        'record_off': {
            'cmd': 'camera/SH',
            'val': '00',
            'timeout': 0.1
        },
        'record_on': {
            'cmd': 'camera/SH',
            'val': '01',
            'timeout': 0.1
        },
        'mode_video': {
            'cmd': 'camera/CM',
            'val': '00',
            'timeout': 0.1
        }
    }
    statusTemplate = {
        'summary': 'notfound', # one of 'notfound', 'off', 'on', or 'recording'
        'power': '?',
        'batt': '?',
        'mode': '?',
        'record': '?',
        'res': '?',
        'fps': '?',
        'fov': '?'
    }
    password = ''
    
    def __init__(self):
        a = 1
    
    def connect(self, ssid, password):
        self.password = password
        print ssid + ':' + password
    
    def getStatus(self):
        status = self.statusTemplate.copy()
        camActive = True
        
        # loop through different status URLs
        for cmd in self.statusMatrix:
            
            # stop sending requests if a previous request failed
            if camActive:
                url = self.statusURL.replace('CMD', cmd).replace('PWD', self.password)
                
                # attempt to contact the camera
                try:
                    response = urlopen(url, timeout=1).read().encode("hex")
                    
                    # loop through different parts that we know how to translate
                    for item in self.statusMatrix[cmd]:
                        args = self.statusMatrix[cmd][item]
                        part = response[args['a']:args['b']]
                        
                        # translate the response value if we know how
                        if 'translate' in args:
                            if part in args['translate']:
                                status[item] = args['translate'][part]
                            else:
                                status[item] = 'translate error (' + part + ')'
                        else:
                            status[item] = part
                except:
                    camActive = False
        
        # build summary
        if status['record'] == 'on':
            status['summary'] = 'recording'
        elif status['power'] == 'on':
            status['summary'] = 'on'
        elif status['power'] == 'off':
            status['summary'] = 'off'
        
        return status
    
    def sendCommand(self, command):
        if command in self.commandMaxtrix:
            args = self.commandMaxtrix[command]
            url = self.commandURL.replace('CMD', args['cmd']).replace('PWD', self.password).replace('VAL', args['val'])
            
            # attempt to contact the camera
            #try:
            print url
            return urlopen(url, timeout=args['timeout']).read()
            #except:
            #    return False
            
        else:
            return False
    
    def test(self):
        self.connect('abortcam1', 'password')
        status = self.getStatus()
        print status
















