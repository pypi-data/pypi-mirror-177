from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple, Optional, Self


@dataclass(frozen=True, order=True)
class Entry:
    """
    Class for log entries
    """
    start_time: datetime
    end_time: datetime
    category: str
    description: str = ''

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError('end_time must be larger than start_time')

    @property
    def duration(self) -> timedelta:
        """
        Returns the duration of the entry
        :return: duration
        """

        return self.end_time - self.start_time

    def to_pair(self) -> Tuple[str, timedelta]:
        """
        Returns a tuple of the form (category, duration)
        :return:
        """

        return self.category, self.duration

    def intersection(self, start_time: Optional[datetime] = None,
                     end_time: Optional[datetime] = None) -> Optional[Self]:
        """
        Returns an intersection of the entry's (start_time, end_time) and the (start_time, end_time)
        :param start_time: Optional[datetime]
        :param end_time: Optional[datetime]
        :return: Optional[Self]
        """

        if start_time: start_time = max(start_time, self.start_time)
        else: start_time = self.start_time

        if end_time: end_time = min(end_time, self.end_time)
        else: end_time = self.end_time

        try: return Entry(start_time, end_time, self.category, self.description)
        except ValueError: pass

    def to_period(self) -> Tuple[datetime, datetime]:
        """
        Returns (start_time, end_time)
        :return: Tuple[datetime, datetime]
        """
        return self.start_time, self.end_time
