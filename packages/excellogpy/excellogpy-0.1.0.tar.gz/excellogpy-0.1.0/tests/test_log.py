import unittest
from logpy.model.log import Log, Entry

from datetime import datetime

entries = [
    Entry(datetime(2022, 11, 8, 13), datetime(2022, 11, 8, 14), 'Category'),
    Entry(datetime(2022, 11, 8, 14), datetime(2022, 11, 8, 15), 'Category'),
    Entry(datetime(2022, 11, 8, 13, 15), datetime(2022, 11, 8, 13, 45), 'Category'),
    Entry(datetime(2022, 11, 8, 12), datetime(2022, 11, 8, 14), 'Category'),
    Entry(datetime(2022, 11, 8, 12, 30), datetime(2022, 11, 8, 13, 30), 'Category'),
    Entry(datetime(2022, 11, 8, 13, 30), datetime(2022, 11, 8, 14, 30), 'Category'),
]


class ConstructorTestCase(unittest.TestCase):

    def test00(self):
        log = Log('Name')
        self.assertEqual(log.name, 'Name')

    def test01(self):
        log = Log()
        self.assertEqual(log.name, '')


class AddEntryTestCase(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def test04(self):
        """
        Conflict test: no conflict
        """

        self.log.add_entry(entries[0])
        self.log.add_entry(entries[1])

    def test05(self):
        """
        Conflict test: A C D B
        """

        with self.assertRaises(ValueError):
            self.log.add_entry(entries[0])
            self.log.add_entry(entries[2])

    def test06(self):
        """
        Conflict test: C A B D
        """

        with self.assertRaises(ValueError):
            self.log.add_entry(entries[0])
            self.log.add_entry(entries[2])

    def test07(self):
        """
        Conflict test: C A D B
        """

        with self.assertRaises(ValueError):
            self.log.add_entry(entries[0])
            self.log.add_entry(entries[3])

    def test08(self):
        """
        Conflict test: A C B D
        """

        with self.assertRaises(ValueError):
            self.log.add_entry(entries[0])
            self.log.add_entry(entries[4])

    def test09(self):
        """
        Conflict test
        """

        with self.assertRaises(ValueError):
            self.log.add_entry(entries[0])
            self.log.add_entry(entries[5])

    def test10(self):
        self.assertEqual(self.log.add_entry(entries[0]), entries[0])


class RangeTestCase(unittest.TestCase):
    log = Log()
    log.add_entry(Entry(datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 11), 'Category'))
    log.add_entry(Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'))
    log.add_entry(Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 15), 'Category'))

    periods = [
        (),
        (datetime(2022, 11, 10, 10),),
        {'end_time': datetime(2022, 11, 10, 15)},
        (datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 15)),
        (datetime(2022, 11, 10, 10, 30), datetime(2022, 11, 10, 14, 30)),
    ]

    ranges = [
        (
            Entry(datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 11), 'Category'),
            Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'),
            Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 15), 'Category')
        ), (
            Entry(datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 11), 'Category'),
            Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'),
            Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 15), 'Category')
        ), (
            Entry(datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 11), 'Category'),
            Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'),
            Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 15), 'Category')
        ), (
            Entry(datetime(2022, 11, 10, 10), datetime(2022, 11, 10, 11), 'Category'),
            Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'),
            Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 15), 'Category')
        ), (
            Entry(datetime(2022, 11, 10, 10, 30), datetime(2022, 11, 10, 11), 'Category'),
            Entry(datetime(2022, 11, 10, 12), datetime(2022, 11, 10, 13), 'Category'),
            Entry(datetime(2022, 11, 10, 14), datetime(2022, 11, 10, 14, 30), 'Category')
        )
    ]

    def test00(self):
        self.assertEqual(tuple(self.log.range(*self.periods[0])), self.ranges[0])

    def test01(self):
        self.assertEqual(tuple(self.log.range(*self.periods[1])), self.ranges[1])

    def test02(self):
        self.assertEqual(tuple(self.log.range(**self.periods[2])), self.ranges[2])

    def test03(self):
        self.assertEqual(tuple(self.log.range(*self.periods[3])), self.ranges[3])

    def test04(self):
        self.assertEqual(tuple(self.log.range(*self.periods[4])), self.ranges[4])
