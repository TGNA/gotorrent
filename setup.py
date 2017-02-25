# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='gotorrent',
    version='0.0.1',
    url='https://github.com/TGNA/gotorrent',
    license='MIT License',
    author='Oscar Blanco, Victor Colome',
    install_requires=['gevent', 'pyactor'],
    test_suite='test',
)