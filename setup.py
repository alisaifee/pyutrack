#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()
import os

this_dir = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = [
    k for k in open(
        os.path.join(this_dir, 'requirements', 'main.txt')
    ).read().splitlines() if k.strip()
]

setup(
    name='pyutrack',
    version='0.1.0',
    description="Command line utility to interface with YouTrack",
    long_description=readme + '\n\n' + history,
    author="Ali-Akber Saifee",
    author_email='ali@indydevs.org',
    url='https://github.com/alisaifee/pyutrack',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'pyu=pyutrack.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="MIT license",
    zip_safe=False,
    keywords='pyutrack',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
