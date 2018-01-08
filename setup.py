#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='istr',
    version='0.9.0',
    description="Case-insensitive string implementation.",
    long_description=readme + '\n\n' + history,
    author="Pedro Algarvio",
    author_email='pedro@algarvio.me',
    url='https://github.com/saltstack/istr',
    packages=['istr'],
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='case-insensitive string match',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
