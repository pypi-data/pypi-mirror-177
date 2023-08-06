#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'rich',
    'inquirer',
    'dacite',
    'pyyaml'
]

setup(
    name='ggist1',
    version='0.1.18',
    description="CLI tool boilerplate using click, please replace!",
    long_description='bla bla',
    author="Moshe Ro",
    author_email='mzsrtgzr2@gmail.com',
    url='https://github.com/mzsrtgzr2/ggist',
    packages=['ggist_cli_app'],
    entry_points={
        'console_scripts': [
            'ggist=ggist_cli_app:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='ggist1',
    classifiers=[
    ]
)
