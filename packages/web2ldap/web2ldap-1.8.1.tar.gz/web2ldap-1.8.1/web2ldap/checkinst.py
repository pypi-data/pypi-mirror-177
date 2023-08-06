# -*- coding: ascii -*-
"""
This script checks all the prerequisites for running
a particular release version of web2ldap.

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import sys
import os
import socket
import platform
import sysconfig
from pprint import pformat

import ldap0
import ldap0.functions

from .log import logger


def check_inst():
    """
    Display Python and OpenLDAP installation details
    """
    logger.debug('*** Environment ***')
    for var in (
            'WEB2LDAP_HOME',
            'LOG_LEVEL',
            'PYTHONPATH',
            'PYTHONDONTWRITEBYTECODE',
            'LDAP0_TRACE_LEVEL',
        ):
        if var in os.environ:
            logger.debug('%s = %r', var, os.environ[var])
    logger.debug('*** Python interpreter ***')
    logger.debug('sys.executable= %r', sys.executable)
    logger.debug('sys.prefix= %r', sys.prefix)
    logger.debug('sys.exec_prefix= %r', sys.exec_prefix)
    logger.debug('sys.version= %r', sys.version)
    logger.debug('sys.version_info= %r', sys.version_info)
    logger.debug('sys.maxunicode = %r (%s)', sys.maxunicode, hex(sys.maxunicode))
    logger.debug('sys.platform= %r', sys.platform)
    try:
        logger.debug('platform.platform()= %r', platform.platform())
    except PermissionError as err:
        logger.warning('Error invoking platform.platform(): %r', err)
    logger.debug('platform.uname()= %r', platform.uname())
    logger.debug('os.name= %r', os.name)
    logger.debug('socket.has_ipv6= %r', socket.has_ipv6)

    if sys.version_info.major < 3:
        logger.error('Unsupported Python version: sys.version_info= %r', sys.version_info)
        raise SystemExit('Unsupported Python version!')

    try:
        platform.libc_ver
    except AttributeError:
        pass
    else:
        logger.debug('platform.libc_ver()= %r', platform.libc_ver())

    logger.debug('*** sysconfig.get_paths() ***\n%s', pformat(sysconfig.get_paths()))
    logger.debug('*** sys.path ***\n%s', pformat(sys.path))
    logger.debug('sysconfig.get_python_version() = %r', sysconfig.get_python_version())
    logger.debug('sysconfig.get_platform() = %r', sysconfig.get_platform())
    logger.debug('sysconfig.is_python_build() = %r', sysconfig.is_python_build())
    logger.debug('sys.getfilesystemencoding() = %r', sys.getfilesystemencoding())

    # Display version numbers of OpenLDAP libs
    logger.debug('*** Imported modules ***')
    logger.debug('ldap0 %s', ldap0.__version__)
    logger.debug('*** OpenLDAP libs ***')
    logger.debug('ldap0.API_VERSION: %s', ldap0.API_VERSION)
    logger.debug('ldap0.VENDOR_VERSION: %s', ldap0.VENDOR_VERSION)
    # Check whether built with SSL/TLS (OpenSSL)
    logger.debug('*** Support for SSL/TLS ***')
    logger.debug('ldap0.TLS_AVAIL = %r', ldap0.TLS_AVAIL)
    logger.debug('ldap0.LIBLDAP_TLS_PACKAGE = %r', ldap0.LIBLDAP_TLS_PACKAGE)
    # Check whether built with SASL (Cyrus-SASL)
    logger.debug('*** SASL support ***')
    logger.debug('ldap0.SASL_AVAIL = %r', ldap0.SASL_AVAIL)
    logger.debug('*** ldap0.OPT_API_INFO ***')
    logger.debug(pformat(ldap0.functions.get_option(ldap0.OPT_API_INFO)))
