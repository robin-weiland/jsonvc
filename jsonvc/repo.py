#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-26"
__version__ = "0.0.0"

__all__ = ('JSONVC',)

"""
Module for simulating version control for json dictionaries
"""

from jsonvc.tools import dump, load, index_from_timestamp, get_diff
from jsonvc.entry import Entry
from jsonvc.diffs import Diff
from pathlib import Path
from datetime import datetime
from functools import wraps
from operator import delitem

from typing import Any, Optional, Union, List, Tuple, Dict, Mapping


def auto_commit(method):
    """
    Automatically add and commit changes made by decorated methods if JSONVC.AUTO_CHANGE is set

    :param method: Method to decorate
    :return: Decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        print(method.__name__.replace('_', ''))
        data = method(self, *args, **kwargs)
        if JSONVC.AUTO_COMMIT:
            self.add()
            self.commit()
        return data
    return wrapper


class JSONVC(dict):
    """jsonvc repo"""

    AUTO_COMMIT: bool = True

    path: Path
    entries: List[Entry]
    diff: Diff
    init_entry_size: int

    def __init__(self, path: Optional[Union[Path, str]] = None, data: Optional[Dict[str, Any]] = None):
        if path: self.path = Path(path)
        super(JSONVC, self).__init__()
        self.load(path, data)
        self.build()

    def load(self, path: Optional[Union[Path, str]], data: Optional[Dict[str, Any]] = None) -> None:
        """
        Load a repo either from a file or raw data.

        :param path: Path to repo file
        :param data: Raw repo data
        :return: Nothing
        """
        if path:
            if not Path(path).exists(): JSONVC.init(path)
            data = load(path)
        if not self.verify(data=data): raise Exception('Not a valid jsonvc file or dataset!')
        self.entries = [Entry(*entry) for entry in data]
        self.diff = Diff()
        self.init_entry_size = len(self.entries)

    def build(self, index: Optional[int] = None, timestamp: Optional[Union[int, datetime]] = None) -> None:
        """
        Build a dict from jsonvc repo either up to index or timestamp entries/commits.

        :param index: Entry index to build the dictionary up to
        :param timestamp: Timestamp to build the dictionary up to
        :return: Nothing
        """
        if index is not None: state = index
        elif timestamp is not None: state = index_from_timestamp(self.entries, timestamp)
        else: state = len(self.entries) - 1

        # TODO use JSONVC.index() above

        if state < 0: return

        if not 0 <= state <= len(self.entries): raise IndexError(f'State {state} was out of range [0, {len(self)}]!')

        super(JSONVC, self).clear()
        counter = 0
        data = dict()
        while state >= counter:
            data = self.entries[counter].apply(data)
            counter += 1

        super(JSONVC, self).update(data)

    def dump(self, path: Union[Path, str] = None, compression=True, **kwargs) -> None:
        """
        Store the jsonvc repo to a file.

        :param path: File to store to [Defaults to JSONVC().path]
        :param compression: Whether to compress the repo
        :param kwargs: json.dumps() kwargs
        :return: Nothing
        """
        if not self.path and not path: raise Exception('Nowhere to dump to!')
        if not self.path: self.path = Path(path)
        dump(self.path,
             [entry.history_entry() for entry in self.entries],
             compression,
             **kwargs)

    def commit(self, path: Union[Path, str] = None) -> bool:
        """
        Commit changes to the repo.

        :param path: File to commit to [Defaults to JSONVC().path]
        :return: Whether there were chamges added
        """
        if len(self.entries) != self.init_entry_size:
            self.dump(path)
            self.build()
            return True
        return False

    def add(self) -> bool:
        """
        Add changes to commit them.

        :return: Whether changes are really different to already commited data
        """
        if self.diff:
            self.entries.append(Entry.from_diff(self.diff))
            return True
        return False

    def revert(self) -> None:
        """Drop uncommited changes."""
        self.diff.reset()
        self.reset(self.init_entry_size)

    @auto_commit
    def reset(self, index: Optional[int] = None, timestamp: Optional[Union[int, datetime]] = None) -> None:
        """
        Remove any commits after either an index or timestamp.

        :param index: Index in the repo entries
        :param timestamp: Timestamp in repo entries
        :return: Nothing
        """
        self.entries = self.entries[:self.index(index, timestamp)]

    @auto_commit
    def strip(self, index: Optional[int] = None, timestamp: Optional[Union[int, datetime]] = None) -> None:
        """
        Remove any commits before either an index or timestamp.

        :param index: Index in the repo entries
        :param timestamp: Timestamp in repo entries
        :return: Nothing
        """
        self.entries = self.entries[self.index(index, timestamp):]

    def index(self, index: Optional[int] = None, timestamp: Optional[Union[int, datetime]] = None) -> int:
        """
        Get an index for commits either from index or timestamp.

        :param index: Index in the repo entries
        :param timestamp: Timestamp in repo entries
        :return: index int
        """
        if index is not None: state = index
        elif timestamp is not None: state = index_from_timestamp(self.entries, timestamp)
        else: state = len(self.entries)

        if not 0 <= state < len(self): raise IndexError(f'State {state} was out of range [0, {len(self)}]!')

        return state

    @property
    def info(self) -> str:
        """Data about the repo"""
        print('diff.changes', self.diff.changes, 'diff.deletions', self.diff.deletions)
        return f'jsonvc-repo[{len(self.entries)} entries, currently {len(self.diff)} changes]'

    @staticmethod
    def init(path: Union[Path, str]) -> None:
        """
        Generate a new jsonvc repo.

        :param path: path to the jsonvc repo
        :return: Nothing
        """
        dump(path, list())

    @staticmethod
    def verify(path: Optional[Union[Path, str]] = None,
               data: Optional[List[List[Union[int, Dict[Any, Any], List[Any]]]]] = None) -> bool:
        """
        Determine wheter a path or data are a valid jsonvc repo.

        :param path: path of the jsonvc repo
        :param data: raw jsonvc repo data
        :return: bool
        """
        try:
            if path: data = load(path)  # path 'stronger' than data
            elif data is None: raise ValueError('Neither path nor data were provided!')
            return isinstance(data, list) \
                and all(map(
                    lambda entry: isinstance(entry, list)
                        and len(entry) == 3
                        and isinstance(entry[0], int)
                        and isinstance(entry[1], dict)
                        and isinstance(entry[2], list),
                        data))
        except Exception as exc: return False and exc  # pycharm doesn't like just Exception

    # dict methods to override

    @auto_commit
    def __setitem__(self, key: Any, value: Any) -> None:
        self.diff[key] = value
        super(JSONVC, self).__setitem__(key, value)

    @auto_commit
    def __delitem__(self, key: Any) -> None:
        del self.diff[key]
        super(JSONVC, self).__delitem__(key)

    @auto_commit
    def update(self, __m: Mapping[Any, Any], **kwargs: Any) -> None:
        changes, deletions, = get_diff(self, dict(__m))
        self.diff.changes.update(changes)
        [delitem(self.diff.changes, key) for key in deletions]
        self.diff.deletions.update(deletions)
        [self.diff.deletions.discard(key) for key in changes.keys()]
        super(JSONVC, self).update(__m, **kwargs)

    @auto_commit
    def pop(self, k: Any) -> Any:
        self.diff.pop(k)
        return super(JSONVC, self).pop(k)

    @auto_commit
    def popitem(self) -> Tuple[Any, Any]:
        try: item = super(JSONVC, self).popitem()
        except KeyError: raise
        self.diff.pop(item[0])
        return item

    @auto_commit
    def setdefault(self, __key: Any, __default: Any = ...) -> Any:
        self.diff.setdefault(__key, __default)
        return super(JSONVC, self).setdefault(__key, __default)

    @auto_commit
    def clear(self) -> None:
        self.diff.clear(self.keys())
        super(JSONVC, self).clear()


if __name__ == '__main__': pass
