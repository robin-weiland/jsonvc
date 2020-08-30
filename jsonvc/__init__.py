#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-25"
__version__ = "0.0.0"

__all__ = ('JSONVC',)

r"""Create json data as a version control like repo.

Store json data as a list of changes and deletions,
beeing able to reset data by index or to a certain
point in time.

Typical usage example:
    
    # load json data as a dict-like object and change its value
    repo = JSONVC('/path/to/repo.jsonvc')
    repo['change'] = True
    
    # by default changes get auto-added and auto-commited
    repo = JSONVC('/path/to/repo.jsonvc')
    repo.update(dict(hello='world'))
    repo.add()
    repo.commit()
"""

from jsonvc.repo import JSONVC
from jsonvc.cli import main as cli


def main() -> None: cli()


if __name__ == '__main__': main()
