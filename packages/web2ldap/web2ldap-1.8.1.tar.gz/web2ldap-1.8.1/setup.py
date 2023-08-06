#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
package/install web2ldap
"""

import sys
import os
from setuptools import setup, find_packages

try:
    import stdeb.util
except ImportError:
    pass
else:
    stdeb.util.RULES_OVERRIDE_INSTALL_TARGET_PY3 += " --install-data /"

PYPI_NAME = 'web2ldap'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

DATA_FILES = sorted([
    (
        root_dir[len(BASEDIR)+1:],
        [
            os.path.join(root_dir[len(BASEDIR)+1:], filename)
            for filename in filenames
        ]
    )
    for root_dir, _, filenames in os.walk(os.path.join(BASEDIR, 'etc', 'web2ldap'))
])

sys.path.insert(0, os.path.join(BASEDIR, 'web2ldap'))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='Full-featured web-based LDAPv3 client',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://www.web2ldap.de',
    download_url='https://www.web2ldap.de/download.html',
    project_urls={
        'Documentation': 'https://web2ldap.de/docs.html',
        'Code': 'https://code.stroeder.com/ldap/web2ldap',
        'Issue tracker': 'https://code.stroeder.com/ldap/web2ldap/issues',
    },
    keywords=['LDAP', 'LDAPv3', 'Web', 'Gateway'],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    test_suite='tests',
    python_requires='>=3.6.*',
    include_package_data=True,
    data_files=DATA_FILES,
    install_requires=[
        'setuptools',
        'ldap0>=1.4.7',
        'asn1crypto',
        'iso3166',
        'xlwt',
        'paramiko',
    ],
    extras_require={
        'image': ["Pillow"],
        'xml': ['defusedxml'],
        'metrics': ['prometheus_client>=0.7.1'],
        'dns': ['dnspython>=2.0.0'],
        'phonenumbers': ['phonenumbers'],
    },
    zip_safe=False,
    entry_points={
        'console_scripts':[
            'web2ldap=web2ldap.__main__:run_standalone',
        ],
        'web2ldap_data':[
            'templates=web2ldapcnf.templates:get_templates_path',
            'properties=web2ldapcnf.templates:get_properties_path',
            'schema=web2ldapcnf.templates:get_schema_path',
        ],
    }
)
