__author__ = 'Chuck Martin'

import os
from setuptools import setup
import roi_crm

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='roi_crm',
    version=roi_crm.__version__,
    packages=['roi_crm'],
    include_package_data=True,
    license='All rights reserved by ROI Technologies LLC',
    description='A simple CRM app for Django',
    long_description=README,
    author='Charles Martin',
    author_email='chuck.martin@roitechnologies.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)