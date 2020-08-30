#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-25"
__version__ = "0.0.0"

__all__ = ('load', 'dump', 'get_diff', 'index_from_timestamp', 'COMPRESSION',)

"""
Collection of tool functions for jsonvc
"""

from jsonvc.entry import Entry
from json import loads, dumps
from pathlib import Path
from gzip import compress, decompress
from binascii import hexlify
from datetime import datetime

from typing import Any, Union, Optional, Tuple, Set, Dict, List

COMPRESSION: bool = True  # aka humanly readable or not


def compression(data: str, comp=COMPRESSION) -> bytes:
    """
    Compress data or just convert it to bytes.

    :param data: The data to compress
    :param comp: Whether to compress or just convert to bytes
    :return: bytes
    """
    return compress(bytes(data, encoding='utf-8')) if comp else bytes(data, encoding='utf-8')


def dump(path: Union[Path, str],
         data: List[List[Union[int, Dict[Any, Any], Set[Any]]]],
         ignore_exist: bool = True,
         comp: bool = COMPRESSION,
         **kwargs) -> None:
    """
    Dump repo data to a file and compress it.

    :param path: File location
    :param data: Data to dump
    :param ignore_exist: Overwrite existing file if set
    :param comp: Whether to compress data
    :param kwargs: json.dump() arguments
    :return: Nothing
    """
    kwargs.update(dict(indent=2))
    path = Path(path)
    if not ignore_exist and path.exists(): return
    path.write_bytes(compression(dumps(data, **kwargs) if isinstance(data, list) else data, comp))


def decompression(data: bytes, use_comp=COMPRESSION) -> str:
    """
    Decompress data or just convert it to str

    :param data: Data to decompress
    :param use_comp: Wheter to decompress or just convert to str
    :return: str
    """
    return decompress(data) if use_comp else data.decode('utf-8')


def load(path: Union[Path, str],
         use_comp=COMPRESSION,
         auto_detect_comp=True,
         **kwargs) -> List[List[Union[int, Dict[Any, Any], Set[Any]]]]:
    """
    Load repo data from a file and decompress it.

    :param path: File location
    :param use_comp: Whether to decompress data
    :param auto_detect_comp: Whether to auto-detect if a repo is compressed
    :param kwargs: json.loads() arguments
    :return: repo data
    """
    try: return loads(decompression(Path(path).read_bytes(), use_comp if not auto_detect_comp else is_compressed(path)),
                      **kwargs)
    except UnicodeDecodeError:
        raise Exception('Failed to read file! Did you attempt to read a compressed file without decompression?')


def get_diff(old: Dict[str, Any], new: Dict[str, Any]) -> Optional[Tuple[Dict[str, Any], Set[Any]]]:
    """
    Get added, changed and deleted values between two dictionaries.

    :param old: The dictionary to compare to
    :param new: The dictionary that gets compared
    :return: differences
    """
    changes = dict()
    for key, value in new.items():
        if key not in old or old[key] == value: continue
        print('KEY:', key)
        changes[key] = value
    for key in new.keys() - old.keys(): changes[key] = new[key]
    deletes = (old.keys() - new.keys())
    return (changes, deletes,) if len(changes) + len(deletes) else None


def is_compressed(path: Union[Path, str]) -> bool:
    """
    Determine whether a repo file is compressed.

    :param path: File location
    :return: bool
    """
    with Path(path).open('rb') as file:
        return hexlify(file.read(2)) == b'1f8b'


def index_from_timestamp(entries: List['Entry'], timestamp: Union[int, datetime]) -> int:
    """
    Get index for a list of repo entries from a timestamp.

    :param entries: Repo entry data
    :param timestamp: Time to compare the entries to
    :return: int
    """
    if isinstance(timestamp, datetime): timestamp = timestamp.timestamp()
    index = -1
    for entry in entries:
        if entry.timestamp > timestamp: break
        index += 1
    return index


if __name__ == '__main__': pass
