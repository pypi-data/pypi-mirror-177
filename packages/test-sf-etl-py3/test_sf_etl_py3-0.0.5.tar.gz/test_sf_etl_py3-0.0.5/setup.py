# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

long_description = 'this is surfin'
if os.path.exists("README.md"):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='test_sf_etl_py3',
    version='0.0.5',
    author='iszzZ',
    author_email='xxx@foxmail.com',
    url='',
    description='surfin test',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['sf_etl_py3'],  # find_packages(),
    install_requires=['imgkit==1.2.2',
                      'oss2==2.16.0',
                      'psycopg2-binary==2.8.6',
                      'pyecharts==1.9.1',
                      'oss2==2.16.0',
                      'requests',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)