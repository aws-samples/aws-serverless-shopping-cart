import sys
import unittest

sys.path.append("..")  # Add application to path
sys.path.append("./layers/")  # Add layer to path

import shared  # noqa: E402  # import from layer


class Tests(unittest.TestCase):
    """
    Example included to demonstrate how to run unit tests when using lambda layers.
    """

    def setUp(self):
        pass

    def test_headers(self):
        self.assertEqual(shared.HEADERS.get("Access-Control-Allow-Credentials"), True)


if __name__ == "__main__":
    unittest.main()
