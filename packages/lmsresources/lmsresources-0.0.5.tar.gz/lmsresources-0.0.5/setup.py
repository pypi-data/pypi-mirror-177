from setuptools import setup, find_packages
setup(name="lmsresources",
version="0.0.5",
description="This package contains resource code for LMS.",
packages=find_packages(),
install_requires=['django', 'requests', 'pymongo'])


# from lmsresources.services_interfaces import admin

# admin.helloWorld()