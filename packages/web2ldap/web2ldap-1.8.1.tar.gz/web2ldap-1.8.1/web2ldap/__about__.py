# -*- coding: ascii -*-
"""
web2ldap.__about__ -- Meta information about web2ldap

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import collections

VersionInfo = collections.namedtuple('VersionInfo', ('major', 'minor', 'micro'))
__version_info__ = VersionInfo(
    major=1,
    minor=8,
    micro=1,
)
__version__ = '.'.join(str(val) for val in __version_info__)
__author__ = 'Michael Stroeder'
__mail__ = 'michael@stroeder.com'
__copyright__ = '(C) 1998-2022 by Michael Str\xf6der <michael@stroeder.com>'
__license__ = 'Apache-2.0'

__all__ = [
    '__version_info__',
    '__version__',
    '__author__',
    '__mail__',
    '__license__',
    '__copyright__',
]
