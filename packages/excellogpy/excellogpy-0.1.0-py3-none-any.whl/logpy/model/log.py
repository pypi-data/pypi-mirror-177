from .entry import Entry

from typing import Optional, Generator, List

from datetime import datetime


class Log:
    name: str
    entries: List[Entry]

    def __init__(self, name: str = ''):
        self.name = name
        self.entries = []

    def add_entry(self, entry: Entry) -> Entry:
        """
        Add an Entry object to the log
        :param entry: Entry
        :return: Entry
        """

        for ENTRY in self.entries:
            if ENTRY.intersection(*entry.to_period()):
                raise ValueError(f'Entry conflict:\nA: {ENTRY}\nB: {entry}')

        self.entries.append(entry)

        return entry

    def range(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Generator:
        """
        Returns a range object with entries that end after the start time and begin before the end time
        :param start_time:
        :param end_time:
        :return:
        """

        for ENTRY in self.entries:
            entry = ENTRY.intersection(start_time=start_time, end_time=end_time)
            if entry:
                yield entry
