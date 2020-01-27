import sys
import unittest
from decimal import Decimal

sys.path.append("..")  # Add application to path
sys.path.append("./layers/build/shared-utils/python")  # Add built layer to path

import shared  # Import from layer


class Tests(unittest.TestCase):
    """
    Example included to demonstrate how to run unit tests when using lambda layers.
    """
    def setUp(self):
        pass

    def test_decimal(self):
        self.assertEqual(shared.handle_decimal_type(Decimal(2.22)), 2.22)


if __name__ == '__main__':
    unittest.main()
