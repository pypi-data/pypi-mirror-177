import unittest
from celebrities_births_erikh import Date

class DateTest(unittest.TestCase):
    
    def setUp(self):
        self.new_date = Date(30, 10, 2021)

    def test_date_valid(self):
        assert self.new_date.is_date_valid(32, 10, 2021) == False

    def test_from_string(self):
        date = '12-10-2021'
        expected_value = Date(12, 10, 2021)
        assert Date.from_string(date) == expected_value

unittest.main(argv=[''], verbosity=2, exit=False)