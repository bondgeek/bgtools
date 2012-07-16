import unittest

from test_utils_dates import TestUtilsDates

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilsDates)
    unittest.TextTestRunner(verbosity=2).run(suite)
    