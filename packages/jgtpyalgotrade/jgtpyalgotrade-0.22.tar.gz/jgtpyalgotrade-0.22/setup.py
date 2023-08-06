#!/usr/bin/env python

# jgtpyalgotrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='jgtpyalgotrade',
    version='0.22',
    description='JGT Python Algorithmic Trading.  Based on work from : Gabriel Martin Becedillas Ruiz',
    long_description='Python library for backtesting stock trading strategies.',
    author='Jean-Guillaume Isabelle',
    author_email='jgtpyalgotrade@guillaumeisabelle.com',
    url='http://github.com/jgwill/jgtpyalgotrade/',
    download_url='https://github.com/jgwill/jgtpyalgotrade/archive/refs/tags/dummy.zip',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=[
        'jgtpyalgotrade',
        'jgtpyalgotrade.barfeed',
        'jgtpyalgotrade.bitcoincharts',
        'jgtpyalgotrade.bitstamp',
        'jgtpyalgotrade.broker',
        'jgtpyalgotrade.dataseries',
        'jgtpyalgotrade.feed',
        'jgtpyalgotrade.optimizer',
        'jgtpyalgotrade.stratanalyzer',
        'jgtpyalgotrade.strategy',
        'jgtpyalgotrade.talibext',
        'jgtpyalgotrade.technical',
        'jgtpyalgotrade.tools',
        'jgtpyalgotrade.twitter',
        'jgtpyalgotrade.utils',
        'jgtpyalgotrade.websocket',
    ],
    install_requires=[
        "matplotlib",
        "numpy",
        "python-dateutil",
        "pytz",
        "requests",
        "retrying",
        "scipy",
        "six",
        "tornado",
        "tweepy",
        "ws4py>=0.3.4",
    ],
    extras_require={
        "TALib":  ["Cython", "TA-Lib"],
    },
)
