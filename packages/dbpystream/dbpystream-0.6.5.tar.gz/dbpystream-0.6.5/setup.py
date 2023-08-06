#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
from setuptools import setup, find_packages
MAJOR = 0
MINOR = 6
MICRO = 5
VERSION = f"{MAJOR}.{MINOR}.{MICRO}"

setup(
	name = "dbpystream",
	version = VERSION,
    author ="songroom",
    long_description_content_type="text/markdown",
	url = 'https://github.com/songroom2016/dbpystream.git',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=[
            'pandas>=0.18.0',
            'requests>=2.0.0',
			'toml >0.10' ,
			'pyzstd >=0.15',
            ],
	packages = find_packages(),
    license="MIT",
    platforms="any",
 
)
