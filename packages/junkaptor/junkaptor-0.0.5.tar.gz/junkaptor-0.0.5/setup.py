# -*- coding: ascii -*-
"""
package/install junkaptor
"""

import sys
import os
from setuptools import setup, find_packages

PYPI_NAME = 'junkaptor'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(BASEDIR, PYPI_NAME))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='Module package for sanitizing data',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://code.stroeder.com/pymod/python-junkaptor',
    download_url='https://pypi.python.org/pypi/%s/' % (PYPI_NAME),
    project_urls={
        'Code': 'https://code.stroeder.com/pymod/python-%s' % (PYPI_NAME),
        'Issue tracker': 'https://code.stroeder.com/pymod/python-%s/issues' % (PYPI_NAME),
    },
    keywords=[],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    package_data = {
        PYPI_NAME: ['py.typed'],
    },
    test_suite='tests',
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
)
