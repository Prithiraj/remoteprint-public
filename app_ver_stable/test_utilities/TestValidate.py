import unittest
from utilities.validate import Validate

class TestValidate(unittest.TestCase):
    def test_isDigit(self):
        with self.assertRaises(ValueError):
            Validate.isDigit(-12)
            Validate.isDigit(2, min_allowed=4)
            
    
    def test_isValidString(self):
        with self.assertRaises(ValueError):
            Validate.isValidString("")
            Validate.isValidString("x")
            Validate.isValidString(1234)
            
    def test_isSet(self):
        a = None
        self.assertEqual(Validate.isSet(a), False)
        b = []
        self.assertEqual(Validate.isSet(b), True)

if __name__ == "__main__":
    unittest.main()
 