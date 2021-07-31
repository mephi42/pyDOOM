import os
import sys
import unittest

from pyDOOM import play


class TestCase(unittest.TestCase):
    def test(self):
        play([sys.argv[0], "-file", os.path.expanduser("~/Downloads/doomu.wad")])


if __name__ == "__main__":
    unittest.main()
