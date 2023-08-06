from setuptools import setup, find_packages
setup(name="lmsresources",
version="0.0.3",
description="This package contains resource code for LMS.",
packages=find_packages(),
install_requires=['django', 'requests', 'pymongo'])