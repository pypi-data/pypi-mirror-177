from setuptools import setup, find_packages
setup(name="lmsresources",
version="0.0.6",
description="Resource code for LMS.",
long_description="This package contains resources, middlewares and services_interfaces code for LMS.",
packages=find_packages(),
install_requires=['django', 'requests', 'pymongo'])


# from lmsresources.services_interfaces import admin

# admin.update_user_request(user_uuid=123, role="OWNER")