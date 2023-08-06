#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
from setuptools import setup, find_packages

setup(
	name = "wowotuo",
	version = "0.6.1",
    author ="songroom",
    author_email = "rustroom@163.com",
    long_description_content_type="text/markdown",
	url = 'https://github.com/songroom2016/dbpystream.git',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=["pandas>=0.28.0"],
	packages = find_packages(),
 
)
