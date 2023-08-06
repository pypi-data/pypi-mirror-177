#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-koopmans',
    version='0.1.0',
    author='Edward Linscott',
    author_email='edwardlinscott@gmail.com',
    maintainer='Edward Linscott',
    maintainer_email='edwardlinscott@gmail.com',
    license='GNU GPL v3.0',
    url='https://github.com/elinscott/pytest-koopmans',
    description='A plugin for testing the koopmans package',
    long_description=read('README.rst'),
    py_modules=['pytest_koopmans'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0', 'numpy>1.21', 'ase-koopmans==0.1.1', 'koopmans>=1.0.0-b.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'koopmans = pytest_koopmans',
        ],
    },
)
