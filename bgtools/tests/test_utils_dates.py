import unittest

from datetime import date

from bgtools.utils.dates import ccyymmdd, parse_date

class TestUtilsDates(unittest.TestCase):

    def test_date_creation(self):
        tests = [
        (19600809, date(1960, 8, 9)),
        ("9/7/1980", date(1980, 9, 7)),
        ("xxx", None),
        ]
        
        for test in tests:
            self.assertEquals(parse_date(test[0]), test[1])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilsDates)
    
    unittest.TextTestRunner(verbosity=2).run(suite)
