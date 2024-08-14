import unittest

from utilities.PrintSupport import PrintSupport

class TestPrintSupport(unittest.TestCase):
    def test_getCPSupportedOutput(self):
        print(PrintSupport.getCPSupportedOutput())
        self.assertIsInstance(PrintSupport.getCPSupportedOutput(), list)
        