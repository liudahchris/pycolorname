# -*- coding: utf-8 -*-

import unittest

from pycolorname.pantone.logodesignteam import LogoDesignTeam


class LogoDesignTeamTest(unittest.TestCase):

    def setUp(self):
        self.uut = LogoDesignTeam()
        self.uut.load(refresh=True)

    def test_data(self):
        self.assertEqual(len(self.uut), 991)

        # We check a few random colors to be sure that things are fine.
        self.assertEqual(self.uut['PMS 245'], (232, 127, 201))
        self.assertEqual(self.uut['PMS 202'], (140, 38, 51))
        self.assertEqual(self.uut['Pantone Cool Gray 5'], (186, 183, 175))
        self.assertEqual(self.uut['PMS 1345'], (255, 214, 145))
        self.assertEqual(self.uut['Pantone Purple'], (191, 48, 181))
