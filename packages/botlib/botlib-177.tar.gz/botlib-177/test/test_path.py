# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"path tests"


import unittest


from bot import fntime


FN = "bot.hdl.Event/1430491cc8a74bd8917049fc080b3d5c/2022-04-11/22:40:31.11"


class TestPath(unittest.TestCase):


    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.11)
