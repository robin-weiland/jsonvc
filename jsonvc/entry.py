#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-25"
__version__ = "0.0.0"

__all__ = ('Entry',)

"""
Entries of commits in jsonvc repos
"""

from jsonvc.diffs import Diff
from functools import total_ordering
from datetime import datetime

from typing import Any, Union, Dict, List, Set


@total_ordering
class Entry:
    """Entries of commits in jsonvc repos."""

    timestamp: int
    diffs: Diff

    __slots__ = ('timestamp', 'diffs',)

    def __init__(self, timestamp: Union[int, datetime], changes: Dict[Any, Any] = None, deletions: Set[Any] = None):
        self.timestamp = timestamp.timestamp() if isinstance(timestamp, datetime) else timestamp
        self.diffs = Diff(changes, deletions)

    @property
    def changes(self) -> Dict[Any, Any]: return self.diffs.changes

    @changes.setter
    def changes(self, value: Dict[Any, Any]) -> None: self.diffs.changes = value

    @property
    def deletions(self): return self.diffs.deletions

    @deletions.setter
    def deletions(self, value: Set[Any]): self.diffs.deletions = value

    def __eq__(self, other: 'Entry') -> bool:
        return self.timestamp == other.timestamp

    def __lt__(self, other: 'Entry') -> bool:
        if other is None: return False
        return self.timestamp < other.timestamp

    def __str__(self) -> str:
        return f'[{self.timestr()}; {len(self.changes)} changes, {len(self.deletions)} deletions]'

    def __repr__(self) -> str:
        return str(self)

    def __or__(self, other: 'Entry') -> 'Entry':
        return self if self > other else other

    def __hash__(self) -> int: return hash(self.timestamp + hash(dict))

    def timestr(self) -> str:
        """
        Get humanly readable time from timestamp.

        :return: str
        """
        return str(datetime.fromtimestamp(self.timestamp)).replace(' ', '--')

    def history_entry(self) -> List[Union[int, Dict[Any, Any], List[Any]]]:
        """
        Get entry as a json serializable format.

        :return: list
        """
        return [self.timestamp, self.changes, list(self.deletions)]

    def apply(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Apply changes from an entry to a dict.

        :param data: dict to apply the changes to
        :return: dict
        """
        data = data.copy()
        data.update(self.changes)
        for d in self.deletions: data.pop(d, None)
        return data

    @classmethod
    def from_diff(cls, diff: Diff) -> 'Entry':
        """
        Get Entry from difference data.

        :param diff: Differences between commits
        :return: Entry
        """
        return cls(int(datetime.now().timestamp()), *diff)


if __name__ == '__main__': pass
