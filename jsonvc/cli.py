#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-25"
__version__ = "0.0.0"

__all__ = ('main',)

from jsonvc.repo import JSONVC
from jsonvc.tools import get_diff
from argparse import ArgumentParser
from json import loads
from sys import stderr
from re import sub

from typing import Union, List

# no pyfiglet for the dependency
intro: str = r"""
_________ _______  _______  _                 _______ 
\__    _/(  ____ \(  ___  )( (    /||\     /|(  ____ \
   )  (  | (    \/| (   ) ||  \  ( || )   ( || (    \/
   |  |  | (_____ | |   | ||   \ | || |   | || |      
   |  |  (_____  )| |   | || (\ \) |( (   ) )| |      
   |  |        ) || |   | || | \   | \ \_/ / | |      
|\_)  )  /\____) || (___) || )  \  |  \   /  | (____/\
(____/   \_______)(_______)|/    )_)   \_/   (_______/
"""

PARSE_REGEX: str = r"""(\w+):\s*(-?\d[\d/.]*)"""


def parse_data(data: Union[List[str], str]) -> str:
    return sub(PARSE_REGEX, r'"\1": "\2"', ''.join(data) if isinstance(data, list) else data)


def main():
    parser = ArgumentParser(prog='jsonvc', description='Tiny version control for json files',
                            epilog=f'jsonvc v{__version__} [{__date__}] by {__author__}')

    parser.add_argument('-ni', '--no-intro', dest='no_intro', action='store_true',
                        help='Do not show the intro.')

    commands = parser.add_subparsers(dest='command', help='Subcommands')

    init = commands.add_parser('init', help='Create new jsonvc "repository".')
    init.add_argument(
            'path',
            nargs=1,
            type=str,
            help='The path to the jsonvc repo.'
        )

    commit = commands.add_parser('commit', help='Commit changes to a jsonvc repo.')
    commit.add_argument(
            'path',
            type=str,
            help='The path to the jsonvc repo.'
        )
    commit.add_argument(
        'data',
        nargs='*',
        type=str,
        help='The new data; must be json serialized string!'
    )

    diff = commands.add_parser('diff', help='Show differences between  the repo [path] and the new data [str]')
    diff.add_argument(
        'path',
        type=str,
        help='The path to the jsonvc repo.'
    )
    diff.add_argument(
        'data',
        nargs='*',
        type=str,
        help='The new data; must be json serialized string!'
    )

    log = commands.add_parser('log', help='Show the history of the jsonvc repo.')
    log.add_argument(
        'path',
        type=str,
        help='The path to the jsonvc repo.'
    )

    reset = commands.add_parser('reset', help='Resets repo to given hash!')
    reset.add_argument(
        'path',
        type=str,
        help='The path to the jsonvc repo.'
    )
    reset.add_argument(
        '-i',
        '--index',
        type=int,
        default=None,
        help='Index for the repo entries to reset to.'
    )
    reset.add_argument(
        '-t',
        '--timestamp',
        type=int,
        default=None,
        help='Timestamp for the repo entries to reset to.'
    )

    strip = commands.add_parser('strip', help='Strip repo history below given hash!')
    strip.add_argument(
        'path',
        type=str,
        help='The path to the jsonvc repo.'
    )
    strip.add_argument(
        '-i',
        '--index',
        # action='store',
        type=int,
        default=None,
        help='Index for the repo entries to strip to.'
    )
    strip.add_argument(
        '-t',
        '--timestamp',
        # action='store',
        type=int,
        default=None,
        help='Timestamp for the repo entries to strip to.'
    )

    branch = commands.add_parser('branch', help='Branches, yeah!')
    branch.add_argument(
        '_',
        nargs='*'
    )

    args = parser.parse_args()

    if not args.no_intro: print(intro, flush=True)

    if args.command == 'branch': stderr.write('NICE TRY!')
    elif args.command == 'log':
        repo = JSONVC(args.path)
        print(repo.info)
        for entry in repo.entries:
            print('\t', entry, sep='')
    elif args.command == 'diff':
        updates, deletions, = get_diff(JSONVC(args.path), loads(parse_data(args.data)))
        print('Differences:')
        if diff is None:
            print('Nothing')
            return
        print('\tUpdates:')
        for key, value, in updates.items(): print(f'\t\t{key}: {value}')
        print()
        print('\tDeletions:')
        for key in deletions: print(f'\t\t{key}')
    elif args.command == 'commit':
        JSONVC(args.path).update(loads(parse_data(args.data)))
        print('Repo updtated and committed.')
    elif args.command == 'reset':
        try:
            JSONVC(args.path).reset(args.index, args.timestamp)
            print('Reset repo.')
        except ValueError:
            stderr.write('Provide index or timestamp!')
            parser.print_help()
        except IndexError:
            stderr.write('Index or timestamp out of range')
    elif args.command == 'strip':
        try:
            JSONVC(args.path).strip(args.index, args.timestamp)
            print('Striped repo.')
        except ValueError:
            stderr.write('Provide index or timestamp!')
            parser.print_help()
        except IndexError:
            stderr.write('Index or timestamp out of range')


if __name__ == '__main__':
    main()
