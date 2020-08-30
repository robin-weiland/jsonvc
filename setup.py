#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-25"
__version__ = "0.0.0"

__all__ = ()

from pathlib import Path
from setuptools import setup, find_packages
from shutil import rmtree

BUILD_DIRS = (
    'jsonvc.egg-info',
    'build',
    'dist'
)


if __name__ == '__main__':
    print('cleaning up')
    for d in BUILD_DIRS:
        path = Path(d)
        if path.exists() and path.is_dir():
            print(f'Deleting {path}...')
            rmtree(d)

    setup(
        name='jsonvc',
        version=__version__,
        packages=find_packages(),
        url='https://github.com/robin-weiland/jsonvc',
        license='MIT',
        author=__author__,
        author_email='robin.weiland@gmx.de',
        description='tiny version control for json data',
        long_description=Path('README.md').read_text(),
        long_description_content_type='text/markdown',
        keywords=['json', 'vcs', 'git'],
        python_requires='>=3.5',  # typing
        classifiers=[
            'Development Status :: 4 - Beta',

            'Environment :: Console',

            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',

            'License :: OSI Approved :: MIT License',

            'Operating System :: OS Independent',

            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',


            'Topic :: Software Development',
            'Topic :: Software Development :: Version Control',
            'Topic:: Scientific / Engineering',
            'Topic :: Scientific/Engineering :: Information Analysis',

            'Typing::Typed'
        ],
        requires=[line.split('=')[0].rstrip('~<>=')
                  for line in Path('requirements.txt').read_text().splitlines()
                  if not (line.startswith('#') or line == '' or line == '\n' or line.endswith('###'))],
        entry_points={
            'console_scripts': [
                'jsonvc = jsonvc:main'
            ]
        }
    )
