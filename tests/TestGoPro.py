#!/usr/bin/env python

import unittest
from gopro import GoPro


class TestGoPro(unittest.TestCase):
    def setUp(self):
        # TODO
        pass

    def test_camera_init(self):
        # initialize a camera object
        camera = GoPro('password')
        self.assertTrue(camera is not None)
