import unittest

from app_ver_1.utilities.PrintSupport import PrintSupport

class TestPrintSupport(unittest.TestCase):
    def test_getCPSupportedOutput(self):
        print(PrintSupport.getCPSupportedOutput())
        self.assertIsInstance(PrintSupport.getCPSupportedOutput(), list)
        