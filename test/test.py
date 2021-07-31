import os
import sys
import unittest

import _pyDOOM


class TestCase(unittest.TestCase):
    def test(self):
        _pyDOOM.main(
            [sys.argv[0], "-file", os.path.expanduser("~/Downloads/doomu.wad")]
        )


if __name__ == "__main__":
    unittest.main()
