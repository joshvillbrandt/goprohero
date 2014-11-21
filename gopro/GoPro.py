#!/usr/bin/python

# GoPro.py
# Josh Villbrandt <josh@javconcepts.com>, Blair Gagnon <blairgagnon@gmail.com>
# August 2013 - November 2014

import logging
import copy
# import cv2
# from PIL import Image
# import StringIO
# import base64

try:
    from urllib.request import urlopen, HTTPError, URLError
except ImportError:
    from urllib2 import urlopen, HTTPError, URLError


class GoPro:
    @staticmethod
    def config():
        return {
            'status': GoPro.statusMatrix,
            'command': GoPro.commandMaxtrix
        }

    @staticmethod
    def _hexToDec(val):
        return int(val, 16)

    def _statusURL(self, command):
        return 'http://{}/{}?t={}'.format(self._ip, command, self._password)

    def _commandURL(self, command, value):
        return 'http://{}/{}?t={}&p=%{}'.format(self._ip, command,
                                                self._password, value)

    def _previewURL(self):
        return 'http://{}:8080/live/amba.m3u8'.format(self._ip)

    timeout = 2.0
    statusMatrix = {
        'bacpac/se': {
            'power': {
                'a': 18,
                'b': 20,
                'translate': {
                    '00': 'sleep',
                    '01': 'on'
                }
            }
        },
        'camera/se': {
            'batt1': {
                'a': 38,
                'b': 40,
                'translate': '_hexToDec'
            }
        },
        'camera/sx': {  # the first 62 bytes of sx are almost the same as se
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
            'fov': {
                'a': 14,
                'b': 16,
                'translate': {
                    '00': '170',
                    '01': '127',
                    '02': '90'
                }
            },
            'picres': {
                'a': 17,
                'b': 18,
                'translate': {
                    '3': '5MP med',
                    '6': '7MP med',
                    '4': '7MP wide',
                    '5': '12MP wide'
                }
            },
            'secselapsed': {
                'a': 26,
                'b': 30,
                'translate': '_hexToDec'
            },
            'orientation': {
                'a': 37,
                'b': 38,
                'translate': {
                    '0': 'up',
                    '4': 'down'
                }
            },
            'charging': {
                'a': 39,
                'b': 40,
                'translate': {
                    '3': 'no',
                    '4': 'yes'
                }
            },
            'mem': {  # i really have no idea what this is
                'a': 42,
                'b': 46,
                'translate': '_hexToDec'
            },
            'npics': {
                'a': 46,
                'b': 50,
                'translate': '_hexToDec'
            },
            'minsremaining': {
                'a': 50,
                'b': 54,
                'translate': '_hexToDec'
            },
            'nvids': {
                'a': 54,
                'b': 58,
                'translate': '_hexToDec'
            },
            'record': {
                'a': 60,
                'b': 62,
                'translate': {
                    '05': 'on',
                    '04': 'off'
                }
            },
            'batt2': {
                'a': 90,
                'b': 92,
                'translate': '_hexToDec'
            },
            'vidres': {
                'a': 100,
                'b': 102,
                'translate': {
                    '00': 'WVGA',
                    '01': '720p',
                    '02': '960p',
                    '03': '1080p',
                    '04': '1440p',
                    '05': '2.7K',
                    '06': '2.7KCin',
                    '07': '4K',
                    '08': '4KCin'
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
            }
        }
    }
    commandMaxtrix = {
        'power': {
            'cmd': 'camera/PW',
            'translate': {
                'sleep': '00',
                'on': '01'
            }
        },
        'record': {
            'cmd': 'camera/SH',
            'translate': {
                'off': '00',
                'on': '01'
            }
        },
        'preview': {
            'cmd': 'camera/PV',
            'translate': {
                'off': '00',
                'on': '02'
            }
        },
        'orientation': {
            'cmd': 'camera/UP',
            'translate': {
                'up': '00',
                'down': '01'
            }
        },
        'mode': {
            'cmd': 'camera/CM',
            'translate': {
                'video': '00',
                'still': '01',
                'burst': '02',
                'timelapse': '03',
                'timer': '04',
                'hdmi': '05'
            }
        },
        'volume': {
            'cmd': 'camera/BS',
            'translate': {
                '0': '00',
                '70': '01',
                '100': '02'
            }
        },
        'locate': {
            'cmd': 'camera/LL',
            'translate': {
                'off': '00',
                'on': '01'
            }
        },
        'delete_last': {
            'cmd': 'camera/DL'
        },
        'delete_all': {
            'cmd': 'camera/DA'
        }
    }
    statusTemplate = {
        'summary': 'notfound',  # 'notfound', 'sleeping', 'on', or 'recording'
        'raw': {}
    }

    def __init__(self, ip='10.5.5.9', password='pass', log_level=logging.INFO):
        self._ip = ip
        self._password = password

        # setup log
        log_format = '%(asctime)s   %(message)s'
        logging.basicConfig(format=log_format, level=log_level)

    def password(self, password=None):
        if password is None:
            return self._password
        else:
            self._password = password

    def status(self):
        status = copy.deepcopy(self.statusTemplate)
        camActive = True

        # loop through different status URLs
        for cmd in self.statusMatrix:

            # stop sending requests if a previous request failed
            if camActive:
                url = self._statusURL(cmd)

                # attempt to contact the camera
                try:
                    response = urlopen(
                        url, timeout=self.timeout).read().encode('hex')
                    status['raw'][cmd] = response  # save raw response

                    # loop through different parts we know how to translate
                    for item in self.statusMatrix[cmd]:
                        args = self.statusMatrix[cmd][item]
                        part = response[args['a']:args['b']]

                        # translate the response value if we know how
                        if 'translate' in args:
                            status[item] = self._translate(
                                args['translate'], part)
                        else:
                            status[item] = part
                except (HTTPError, URLError):
                    camActive = False

        # build summary
        if 'record' in status and status['record'] == 'on':
            status['summary'] = 'recording'
        elif 'power' in status and status['power'] == 'on':
            status['summary'] = 'on'
        elif 'power' in status and status['power'] == 'sleep':
            status['summary'] = 'sleep'

        logging.info('GoPro.status() - result {}'.format(status))
        return status

    # def image(self):
    #     try:
    #         # use OpenCV to capture a frame and store it in a numpy array
    #         stream = cv2.VideoCapture(self._previewURL())
    #         success, numpyImage = stream.read()

    #         if success:
    #             # use Image to save the image to a file, but actually save it
    #             # to a string
    #             image = Image.fromarray(numpyImage)
    #             output = StringIO.StringIO()
    #             image.save(output, format='PNG')
    #             str = output.getvalue()
    #             output.close()

    #             logging.info('GoPro.image() - success!')
    #             return 'data:image/png;base64,'+base64.b64encode(str)
    #     except:
    #         pass

    #     # catchall return statement
    #     logging.warning('GoPro.image() - failure')
    #     return False

    def command(self, command, value=None):
        func_str = 'GoPro.command({}, {})'.format(command, value)

        if command in self.commandMaxtrix:
            args = self.commandMaxtrix[command]
            if value is not None and value in args['translate']:
                value = args['translate'][value]
            url = self._commandURL(args['cmd'], value)

            # attempt to contact the camera
            try:
                urlopen(url, timeout=self.timeout).read()
                logging.info('{} - http success!'.format(func_str))
                return True
            except HTTPError as e:
                logging.warning('{} - HTTPError opening {}: {}'.format(
                    func_str, url, e.code))
            except URLError as e:
                logging.warning('{} - URLError opening {}: {}'.format(
                    func_str, url, e.args))
            else:
                logging.warning('{} - other error opening {}'.format(
                    func_str, url))

        # catchall return statement
        return False

    def _translate(self, config, value):
        if isinstance(config, dict):
            # use a lookup dictionary
            if value in config:
                return config[value]
            else:
                return 'translate error: {} not found'.format(value)
        else:
            # use an internal function
            if hasattr(self, config):
                return getattr(self, config)(value)
            else:
                return 'translate error: {} not a function'.format(value)
