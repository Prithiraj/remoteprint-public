import unittest
from app_ver_1.utilities.convert import Convert

class TestConvert(unittest.TestCase):
    def test_toInt(self):
        self.assertIsInstance(Convert.toInt(''), int)
        self.assertEqual(Convert.toInt(10), 10)
        self.assertEqual(Convert.toInt('10'), 10, "1st value and 2nd value are not equal.")
        self.assertEqual(Convert.toInt(None), 0)
        self.assertEqual(Convert.toInt([]), 0)


if __name__ == "__main__":
    unittest.main()