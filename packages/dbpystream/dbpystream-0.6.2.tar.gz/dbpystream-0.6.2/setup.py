#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
from setuptools import setup, find_packages
def get_install_requires():
    reqs = [
            'pandas>=0.18.0',
            'requests>=2.0.0',
			'pickle',
			'toml' ,
			'uuid',
			'json',
			'itertools',
			'random',
			'threading',
			'pyzstd >=0.15',
			'numpy>=1.9.2'
            ]
    return reqs
setup(
	name = "dbpystream",
	version = "0.6.2",
    author ="songroom",
    long_description_content_type="text/markdown",
	url = 'https://github.com/songroom2016/dbpystream.git',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
	packages = find_packages(),
 
)
