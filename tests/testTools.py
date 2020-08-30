#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-30"
__version__ = "0.0.0"

__all__ = ()

from pathlib import Path
import jsonvc.tools
import jsonvc.entry
from os.path import exists
from json import loads, dumps
from datetime import datetime
from gzip import compress, decompress
from random import randint, choice
from operator import add, sub
from string import ascii_letters
from pyfakefs.fake_filesystem_unittest import TestCase


def generate_random_test_data():
    if choice((True, False,)):
        return str([choice(ascii_letters) for _ in range(randint(1, 20))])
    else: return randint(0, 5_000)


class ToolsTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs(modules_to_reload=[jsonvc.tools, jsonvc.entry])

    def test_dump(self):
        path_compress = 'compressed_dump.jsonvc'
        path_uncompress = 'uncompressed_dump.jsonvc'
        data = [[1598787392, dict(), tuple()]]

        self.assertFalse(exists(path_uncompress))
        jsonvc.tools.dump(path_uncompress, data, comp=False)
        self.assertTrue(exists(path_uncompress))
        self.assertEqual(
            dumps(data),
            # ugly
            Path(path_uncompress).read_text().replace('\n', '').replace(' ', '').replace(',', ', '),
            'Not dumped properly!'
        )

        # TODO work this out
        # self.assertFalse(exists(path_compress))
        # jsonvc.tools.dump(path_compress, data)
        # self.assertTrue(exists(path_compress))
        # self.assertEqual(
        #     compress(bytes(dumps(data), encoding='utf-8')),
        #     Path(path_compress).read_bytes(),
        #     'Not dumped properly!'
        # )

    def test_load(self):
        # TODO add another test
        path_compress = 'compressed_load.jsonvc'
        path_uncompress = 'uncompressed_load.jsonvc'
        path_error = 'error_load.jsonvc'
        data = [[1598787392, dict(), tuple()]]

        self.fs.create_file(path_error, contents=compress(bytes(dumps(data), encoding='utf-8')))

        try:
            print(jsonvc.tools.load(path_error, use_comp=False, auto_detect_comp=False))
        except Exception as ex:
            self.assertEqual(str(ex),
                             'Failed to read file! Did you attempt to read a compressed file without decompression?')
        else: self.fail('Should have raised an Exception!')

    def test_diff(self):
        self.assertEqual(
            None,
            jsonvc.tools.get_diff(dict(), dict()),
            'Two empty dicts do not return None diffs!'
        )

        self.assertEqual(
            (dict(), {'a', 'b', 'c'},),
            jsonvc.tools.get_diff(dict(a=1, b=2, c=3), dict()),
            'Differences with an empty dictionary do not resuslt in just deletions!'
        )

        self.assertEqual(
            (dict(a=1, b=2, c=3), set(),),
            jsonvc.tools.get_diff(dict(), dict(a=1, b=2, c=3)),
            'Differences between an empty dictionary do not resuslt in just changes!'
        )

    def test_compression(self):
        self.assertEqual(
            b'data',
            jsonvc.tools.compression('data', comp=False),
            'Data was wrongfully compressed!'
        )

        self.assertEqual(
            compress(b'data'),
            jsonvc.tools.compression('data'),
            'Data was wrongfully not compressed!'
        )

    def test_decompression(self):
        self.assertEqual(
            'data',
            jsonvc.tools.decompression(b'data', use_comp=False),
            'Data was wrongfully decompressed!'
        )

        self.assertEqual(
            decompress(compress(b'data')),
            jsonvc.tools.decompression(compress(b'data')),
            'Data was wrongfully not decompressed!'
        )

    def test_is_compressed(self):
        path_uncompressed = 'uncompressed.jsonvc'
        path_compressed = 'compressed.jsonvc'
        path_random = 'random.png'

        self.fs.create_file(path_uncompressed, contents='[1598787392, {}, ()]')
        self.fs.create_file(path_compressed, contents=jsonvc.tools.compression('[1598787392, {}, ()]', comp=True))
        self.fs.create_file(
            path_random,
            contents=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
                     b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00'
                     b'\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82')

        self.assertFalse(
            jsonvc.tools.is_compressed(path_uncompressed),
            'Uncompressed file was falsely deemed compressed!'
        )

        self.assertTrue(
            jsonvc.tools.is_compressed(path_compressed),
            'Compressed file was falsely deemed uncompressed!'
        )

        # test with unknown data, should return false... I guess

        self.assertFalse(
            jsonvc.tools.is_compressed(path_random),
            'Random data was deemed compressed!'
        )

    def test_index_from_timestamp(self):
        empty_entries = list()
        now = datetime.now().timestamp()
        ops = [add, sub]
        entries = list()
        for i in range(randint(10, 20)):
            entries.append(
                jsonvc.entry.Entry(
                    choice(ops)(now, randint(0, 50_000_000)),
                    dict((generate_random_test_data(), generate_random_test_data()) for _ in range(randint(0, 20))),
                    set(generate_random_test_data() for _ in range(randint(0, 10)))
                )
            )
        entries = sorted(entries)

        entry_index = randint(0, len(entries) - 1)
        entry = entries[entry_index]

        index = jsonvc.tools.index_from_timestamp(entries, entry.timestamp)

        self.assertEqual(
            entry_index,
            index,
            f'Wrong index {index} for {entry} at {entry_index}'
        )

        self.assertEqual(
            -1,
            jsonvc.tools.index_from_timestamp(empty_entries, entry.timestamp),
            'No entry should be found in an empty repo!'
        )


if __name__ == '__main__': pass
