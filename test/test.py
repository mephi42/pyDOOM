import os
import sys
import unittest

import _pyDOOM


class TestCase(unittest.TestCase):
    def test(self):
        with _pyDOOM.init(
            [sys.argv[0], "-file", os.path.expanduser("~/Downloads/doomu.wad")]
        ):
            while True:
                _pyDOOM.step()


if __name__ == "__main__":
    unittest.main()
