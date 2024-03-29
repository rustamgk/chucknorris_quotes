#!/usr/bin/env python
## https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
import typing
import os

from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as fp:
        long_description = fp.read()
except FileNotFoundError:
    long_description = ''

tests_requirements = [
    'pytest',
    'pytest-runner',
    'mock;python_version<="3.3"',
    'autopep8',
    'flake8',
    'pylint',
    'requests-mock',
]

setup(
    name='chucknorris-webapp',
    version='0.0.1',
    description='chucknorris-webapp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={
        '': ['*.html', ]
    },
    install_requires=[
        'typing;python_version<"3.5"',
        'cached_property',
        'flask==1.1.1',
        'flask-caching',
        'requests',
    ],
    extras_require={
        'gunicorn': [
            'gunicorn',
        ],
        'tests': tests_requirements,
    },
    dependency_links=[
    ],
    setup_requires=[
    ],
    tests_require=tests_requirements,
    test_suite='tests',
)
