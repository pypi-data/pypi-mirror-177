# This file is placed in the Public Domain.


"path tests"


import unittest


from opl import fntime


FN = "~/.opbot/store/op.obj.Object/85db943ed1d6491ab17b51510f659caf/2022-11-10/06:06:23.295736"


class TestPath(unittest.TestCase):


    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1668056783.295736)
