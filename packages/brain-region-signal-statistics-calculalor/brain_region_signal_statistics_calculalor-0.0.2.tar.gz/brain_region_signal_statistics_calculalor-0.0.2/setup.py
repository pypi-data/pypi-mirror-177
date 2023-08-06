#!/usr/bin/env python

from setuptools import setup

from os import path
DIR = path.dirname(path.abspath(__file__))

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='brain_region_signal_statistics_calculalor',
    version='0.0.2',
    description='Compute brain region signal statistics for 3D brain volume',
    py_modules=["brain_region_signal_statistics_calculalor"],
    package_dir={'': 'volume_statistics_calculalor'},
    author='Di Wang',
    author_email='di-wang@uiowa.edu',
    url='https://github.com/daisydiwang/brain_region_signal_statistics_calculalor',
    keywords=['3D brain image', 'statistics', 'hierarchical structure'],
    long_description_content_type='text/markdown',
    long_description=README,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'numpy', 
        'pandas',
    ]
)
