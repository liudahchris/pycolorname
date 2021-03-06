# -*- coding: utf-8 -*-

import os
import pickle
import pprint
import unittest

from pycolorname.pantone.cal_print import CalPrint
from pycolorname.pantone.pantonepaint import PantonePaint
from pycolorname.pantone.logodesignteam import LogoDesignTeam
from pycolorname.ral.classic.wikipedia import Wikipedia


class DeprecationTest(unittest.TestCase):
    """
    This class is used to test whether the library has a whole is backward
    compatible. Hence, this is actually a functional test rather than a
    unittest.
    """

    def get_pkl_colors(self, filename):
        with open(os.path.join(os.path.dirname(__file__),
                               "old_pkl_files",
                               filename), 'rb') as fp:
            pkl_colors = pickle.load(fp)
        return pkl_colors

    def compare_dicts(self, dict1, dict2):
        """
        Helper function to compare dicts. Useful to get good statistics of
        why two dicts are not equal - especially when the two dicts are huge.
        """
        keys1, keys2 = set(dict1.keys()), set(dict2.keys())
        if keys1 != keys2:
            msg = ("Length of keys were different: {0} and {1}.\n"
                   "{2} keys found that were common.\n"
                   "dict1 has the following extra items: {3}\n"
                   "dict2 has the following extra items: {4}\n"
                   .format(len(keys1), len(keys2), len(keys1 & keys2),
                           pprint.pformat({k: dict1[k]
                                           for k in keys1 - keys2}),
                           pprint.pformat({k: dict2[k]
                                           for k in keys2 - keys1})))
            raise AssertionError(msg)
        self.assertEqual(dict1, dict2)

    def test_pantone_pantonepaint(self):
        pkl_colors = self.get_pkl_colors("PMS_pantonepaint_raw.pkl")
        new_comparable_colors = {}

        for name, color in PantonePaint().items():
            # Two color names are not there in the earlier set
            if name in ("PMS 13-1520 TPX (Rose Quartz)",
                        "PMS 15-3919 TPX (Serenity)"):
                continue

            # Earlier there was an extra Pantone which has been removed from
            # the site now. This is unnecessary as we already have a PMS at
            # the beginning
            name = name[:-1] + " Pantone" + name[-1:]

            # Earlier "&amp;" was not being converted to "&". Now it is.
            name = name.replace("&", "&amp;")

            # Earlier unicode characters like "é" were taken as "?".
            name = name.encode("ascii", errors="replace").decode("utf-8")

            # There were typos earlier in the website.
            # Use the typo version again for comparison.
            if name == "PMS 19-4118 TPX (Dark Denim Pantone)":
                name = name.replace("Denim", "Derim")
            elif name == "PMS 16-0439 TPX (Spinach Green Pantone)":
                name = name.replace("Spinach", "spinach")
            elif name == "PMS 16-1343 TPX (Autumn Sunset Pantone)":
                name = name.replace("Sunset", "Sunst")
            elif name == "PMS 17-0000 TPX (Frost Gray Pantone)":
                name = name.replace("Gray", "Gary")
            elif name == "PMS 18-0601 TPX (Charcoal Gray Pantone)":
                name = name.replace("Charcoal", "Chalcoal")

            new_comparable_colors[name] = color

        self.compare_dicts(pkl_colors, new_comparable_colors)

    def test_pantone_logodesignteam(self):
        pkl_colors = self.get_pkl_colors("PMS_logodesignteam_raw.pkl")
        new_comparable_colors = {}
        for name, color in LogoDesignTeam().items():
            new_comparable_colors[name] = color
        self.compare_dicts(pkl_colors, new_comparable_colors)

    def test_pantone_cal_print(self):
        pkl_colors = self.get_pkl_colors("PMS_cal-print.pkl")
        new_colors = CalPrint()

        common_color_names = set(pkl_colors.keys()) & set(new_colors.keys())
        self.assertEqual(len(common_color_names), 656)
        self.assertEqual(len(pkl_colors.keys()), 992)
        self.assertEqual(len(new_colors.keys()), 992)

        # Now get all the values which actually had variable names
        # This is done because the delta_e implementation has changed in
        # colormath
        pkl_named_colors = {}
        for name, color in pkl_colors.items():
            if not name.startswith("Pantone"):
                continue
            pkl_named_colors[name] = color
        new_named_colors = {}
        for name, color in new_colors.items():
            if not name.startswith("Pantone"):
                continue
            new_named_colors[name] = color

        self.assertEqual(len(pkl_named_colors.keys()), 57)
        self.assertEqual(len(new_named_colors.keys()), 57)
        self.compare_dicts(pkl_named_colors, new_named_colors)

    def test_ral_classic_wikipedia(self):
        # The earlier names were wrong. They had the section names in
        # wikipedia. i.e. a lot of colors have the name "Yellow/Beige"
        # while wikipedia does provide give better names like "Beige",
        # "Sand yellow", etc. for those colors.
        # So we're removing that part and not checking it.
        comparable_chars = len("RAL 1000")

        pkl_compatible_colors = {}
        for name, color in self.get_pkl_colors("RAL_wikipedia.pkl").items():
            name = name[:comparable_chars]
            pkl_compatible_colors[name] = color

        new_comparable_colors = {}
        for name, color in Wikipedia().items():
            name = name[:comparable_chars]
            # 90xx arent there in the older version except 9003, 9005
            if (name.startswith("RAL 90") and
                    name not in ("RAL 9003", "RAL 9005")):
                continue
            new_comparable_colors[name] = color

        self.compare_dicts(pkl_compatible_colors, new_comparable_colors)
