#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-29"
__version__ = "0.0.0"

__all__ = ('Diff',)

"""
Differences in jsonvc repos
"""

from typing import Any, Optional, Union, Tuple, Dict, Set, Iterator, KeysView


class Diff:
    """jsonvc difference container"""

    changes: Dict[Any, Any]
    deletions: Set[Any]

    __slots__ = ('changes', 'deletions',)

    def __init__(self, changes: Optional[Dict[Any, Any]] = None, deletions: Optional[Set[Any]] = None):
        self.changes = changes or dict()
        self.deletions = deletions or set()

    def merge(self, other: 'Diff') -> None:
        """
        Merge two Diffs together.

        :param other: Diff to merge with
        :return: Nothing (merge in-place)
        """
        [self.deletions.discard(key) for key in other.changes.keys()]
        self.deletions.update(other.deletions)
        self.changes.update(other.changes)
        [self.changes.pop(key, None) for key in self.deletions]

    def __bool__(self) -> bool: return bool(len(self))

    def __str__(self) -> str: return f'Diff[{len(self.changes)} changes, {len(self.deletions)} deletions]'

    def __repr__(self) -> str: return str(self)

    def __len__(self) -> int: return len(self.changes) + len(self.deletions)

    def __eq__(self, other: 'Diff') -> bool:
        return isinstance(other, Diff) and self.changes == other.changes and self.deletions == other.deletions

    def __iter__(self) -> Iterator[Union[dict, set]]: return iter((self.changes, self.deletions,))

    def reset(self) -> None:
        """
        Drop any changes stored in the Diff object.

        :return: Nothing
        """
        self.changes.clear()
        self.deletions.clear()

    # Methods to change diffs, by mimicing a dict

    def __setitem__(self, key: Any, value: Any) -> None:
        self.changes[key] = value
        self.deletions.discard(key)

    def __delitem__(self, key: Any) -> None:
        self.changes.pop(key, None)
        self.deletions.add(key)

    def update(self, current: Dict[Any, Any], updates: Dict[Any, Any]) -> None: pass

    def pop(self, k: Any) -> None:
        self.changes.pop(k, None)
        self.deletions.add(k)

    # popitem() gets handled by pop()

    def setdefault(self, __key: Any, __default: Any = ...) -> None:
        if __key not in self.changes: self.changes[__key] = __default

    def clear(self, keys: Union[KeysView, Tuple[Any, ...]]) -> None:
        self.changes.clear()
        self.deletions.update(keys)


if __name__ == '__main__': pass
