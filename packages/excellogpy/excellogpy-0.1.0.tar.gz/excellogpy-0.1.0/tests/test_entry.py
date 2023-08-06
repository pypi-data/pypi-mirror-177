import unittest
from logpy.model.entry import Entry
from datetime import datetime, timedelta

start_time = datetime(2022, 11, 7, 17)
end_time = datetime(2022, 11, 7, 18)
category = 'Category'
description = 'Description'

duration = timedelta(hours=1)

pair = (category, duration)


class ConstructorTestCase(unittest.TestCase):
    def test00(self):
        entry = Entry(start_time, end_time, category, description)
        self.assertEqual(entry.start_time, start_time)
        self.assertEqual(entry.end_time, end_time)
        self.assertEqual(entry.category, category)
        self.assertEqual(entry.description, description)

    def test01(self):
        entry = Entry(start_time, end_time, category)
        self.assertEqual(entry.start_time, start_time)
        self.assertEqual(entry.end_time, end_time)
        self.assertEqual(entry.category, category)
        self.assertEqual(entry.description, '')

    def test02(self):
        with self.assertRaises(ValueError):
            entry = Entry(end_time, start_time, category)

    def test03(self):
        with self.assertRaises(ValueError):
            entry = Entry(start_time, start_time, category)


class DurationTestCase(unittest.TestCase):

    def test00(self):
        entry = Entry(start_time, end_time, category)
        self.assertEqual(entry.duration, duration)


class ToPairTestCase(unittest.TestCase):

    def test00(self):
        entry = Entry(start_time, end_time, category)
        self.assertEqual(entry.to_pair(), pair)


periods = (
    (datetime(2022, 11, 8, 13), datetime(2022, 11, 8, 14)),
    (datetime(2022, 11, 8, 14), datetime(2022, 11, 8, 15)),
    (datetime(2022, 11, 8, 13, 15), datetime(2022, 11, 8, 13, 45)),
    (datetime(2022, 11, 8, 12), datetime(2022, 11, 8, 14)),
    (datetime(2022, 11, 8, 12, 30), datetime(2022, 11, 8, 13, 30)),
    (datetime(2022, 11, 8, 13, 30), datetime(2022, 11, 8, 14, 30)),
)

entry = Entry(datetime(2022, 11, 8, 13), datetime(2022, 11, 8, 14), 'Category')


class IntersectionTestCase(unittest.TestCase):

    def test00(self):
        """AC BD"""
        self.assertEqual(entry.intersection(*periods[0]), entry)

    def test01(self):
        """A B C D"""
        self.assertEqual(entry.intersection(*periods[1]), None)

    def test02(self):
        """A C D B"""
        self.assertEqual(entry.intersection(*periods[2]), Entry(periods[2][0], periods[2][1], entry.category))

    def test03(self):
        """C A B D"""
        self.assertEqual(entry.intersection(*periods[3]), entry)

    def test04(self):
        """C A D B"""
        self.assertEqual(entry.intersection(*periods[4]), Entry(entry.start_time, periods[4][1], entry.category))

    def test05(self):
        """A C B D"""
        self.assertEqual(entry.intersection(*periods[5]), Entry(periods[5][0], entry.end_time, entry.category))


class ToPeriodTestCase(unittest.TestCase):

    def test00(self):
        self.assertEqual(entry.to_period(), (datetime(2022, 11, 8, 13), datetime(2022, 11, 8, 14)))
