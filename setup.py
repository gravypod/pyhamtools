#!/usr/bin/env python
from setuptools import setup

req = ['pyqrz','pykml','requests']

setup(name="pyporktools",
	packages=["pyporktools"],
	version="0.0.1",
	description="A python3 implementation of hamtools",
	author="Joshua D. Katz",
	author_email="gravypod@gravypod.com",
	install_requires=req,
)
