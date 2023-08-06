#!/usr/bin/env python
"""setup.py for cmempy."""

from setuptools import setup, find_packages

setup(
    name='cmem_cmempy',
    version='22.2',
    author='eccenca',
    author_email='cmempy-developer@eccenca.com',
    maintainer='Sebastian Tramp',
    maintainer_email='sebastian.tramp@eccenca.com',
    url='https://eccenca.com/go/cmempy',
    description='API wrapper for eccenca Corporate Memory',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='Apache 2.0',
    install_requires=[
        "certifi",
        "pyparsing",
        "pysocks",
        "rdflib",
        "requests",
        "requests_toolbelt",
        "six"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Testing',
        'Topic :: Database',
        'Topic :: Utilities',
    ],
)
