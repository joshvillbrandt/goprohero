#!/usr/bin/env python

import unittest
from goprohero import GoProHero


class TestGoPro(unittest.TestCase):
    def setUp(self):
        # TODO
        pass

    def test_camera_init(self):
        # initialize a camera object
        camera = GoProHero('password')
        self.assertTrue(camera is not None)
