#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-04-04 15:48:44
# @Author  : Andranik Sargsyan (and.sargsyan@yahoo.com)
# @Link    : https://github.com/AndranikSargsyan/pylsd-nova
# @Version : 0.0.1

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pylsd-nova-mac-arm',
    version='1.2.0',
    author='Andranik Sargsyan',
    author_email='and.sargsyan@yahoo.com',
    description='Fork of pylsd-nova that supports MAC arm (m1)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD',
    keywords='LSD',
    url='https://github.com/AndranikSargsyan/pylsd-nova',
    packages=['pylsd', 'pylsd.bindings', 'pylsd.lib'],
    package_dir={'pylsd.lib': 'pylsd/lib'},
    package_data={'pylsd.lib': [
        'darwin/arm64/*.dylib',
        'darwin/x64/*.dylib',
        'win32/x86/*.dll',
        'win32/x64/*.dll',
        'linux/*.so'
    ]},
)
