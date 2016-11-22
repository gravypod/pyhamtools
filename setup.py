#!/usr/bin/env python

from distutils.core import setup

setup(name="pyhamtools",
	version="0.0.1",
	description="A python3 implementation of hamtools",
	author="Joshua D. Katz",
	author_email="gravypod@gravypod.com",
	packages=["pyhamtools"],
	install_requires=["cachetools", "pykml"]
)
