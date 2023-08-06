# -*- coding: ascii -*-
"""
web2ldap.log -- Logging

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import os
import sys
import logging
import pprint
import collections
from typing import Dict

from .__about__ import __version__


LOG_LEVEL = os.environ.get('LOG_LEVEL', '').upper() or logging.INFO

LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'

HTTP_ENV_VARS = {
    'CONTENT_LENGTH',
    'CONTENT_TYPE',
    'PATH_INFO',
    'QUERY_STRING',
    'REQUEST_METHOD',
    'SCRIPT_NAME',
    'SERVER_NAME',
    'SERVER_PORT',
}

EXC_TYPE_COUNTER: Dict[str, int] = collections.defaultdict(lambda: 0)


class LogHelper:
    """
    mix-in class for logging with a class-specific log prefix
    """

    def _log_prefix(self):
        return '%s[%x]' % (self.__class__.__name__, id(self))

    def log(self, level, msg, *args, **kwargs):
        logger.log(level, ' '.join((self._log_prefix(), msg)), *args, **kwargs)


def log_exception(env, ls, dn, debug):
    """
    Write an exception with environment vars, LDAP connection data
    and Python traceback to error log
    """
    # Get exception instance and traceback info
    exc_type, exc_value, exc_trb = sys.exc_info()
    global EXC_TYPE_COUNTER
    exc_key = '%s.%s' % (exc_type.__module__, exc_type.__name__)
    EXC_TYPE_COUNTER[exc_key] += 1
    logentry = [
        '--------------------------- Unhandled error ---------------------------',
        'web2ldap %s' % (__version__,),
        '%s raised %d times' % (exc_type, EXC_TYPE_COUNTER[exc_key]),
        'LDAPSession instance: %r' % (ls,),
        'DN: %s' % (dn,),
        '%s.%s: %s' % (exc_type.__module__, exc_type.__name__, exc_value),
    ]
    if debug and ls is not None:
        # Log the LDAPSession object attributes
        logentry.append(pprint.pformat([
            (attr, getattr(ls, attr))
            for attr in ls.__slots__
            if hasattr(ls, attr)
        ]))
    if debug:
        # Log all environment vars
        logentry.append(pprint.pformat(sorted([
            (name, val)
            for name, val in env.items()
            if (
                name in HTTP_ENV_VARS or
                name.startswith('HTTP') or
                name.startswith('REMOTE') or
                name.startswith('X-_') or
                name.startswith('SSL_')
            )
        ])))
    # Write the log entry
    logger.error(os.linesep.join(logentry), exc_info=debug)
    # explicitly remove stuff
    del exc_type
    del exc_value
    del exc_trb
    # end of log_exception()


def init_logger():
    """
    Create logger instance
    """
    if 'LOG_CONFIG' in os.environ:
        from logging.config import fileConfig
        fileConfig(os.environ['LOG_CONFIG'])
    else:
        logging.basicConfig(
            level=LOG_LEVEL,
            format=LOG_FORMAT,
            datefmt=LOG_DATEFMT,
        )
    _logger = logging.getLogger(os.environ.get('LOG_QUALNAME', None))
    _logger.name = 'web2ldap'
    return _logger


global logger
logger = init_logger()
