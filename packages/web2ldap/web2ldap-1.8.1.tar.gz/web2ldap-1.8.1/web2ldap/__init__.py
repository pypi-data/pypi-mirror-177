# -*- coding: ascii -*-
"""
web2ldap application package

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import sys
import os
import logging
import time
import platform

from .log import logger, LogHelper
from .__about__ import __version__

# FIX ME! For now we'll strictly block module h2 from loading because
# it's seriously broken and does not run in strict byte mode (python3 -bb)
# see https://github.com/python-hyper/h2/issues/1236
sys.modules['h2'] = None

# Path name of [web2ldap]/etc/web2ldap
if 'WEB2LDAP_HOME' in os.environ:
    # env var points to web2ldap root prefix directory,
    # assume configuration is in a sub-directory etc/web2ldap therein
    ETC_DIR = os.path.join(os.environ['WEB2LDAP_HOME'], 'etc', 'web2ldap')
elif (
        platform.uname().system == 'Linux'
        and sys.prefix == '/usr'
    ):
    # OS-wide installation on GNU/Linux,
    # assume configuration is in global /etc/web2ldap
    ETC_DIR = '/etc/web2ldap'
else:
    # assume configuration is in a sub-directory etc/web2ldap
    # within system-prefix directory (e.g. in virtual env or on *BSD)
    ETC_DIR = os.path.join(sys.prefix, 'etc', 'web2ldap')
sys.path.append(ETC_DIR)

# Default directory for [web2ldap]/etc/web2ldap/templates
TEMPLATES_DIR = os.path.join(ETC_DIR, 'templates')

STARTUP_TIME = time.time()

logger.info('Starting web2ldap %s', __version__)
logger.debug('ETC_DIR = %r', ETC_DIR)
logger.debug('TEMPLATES_DIR = %r', TEMPLATES_DIR)


def cmp(val1, val2):
    """
    Workaround to have cmp() like in Python 2
    """
    return bool(val1 > val2) - bool(val1 < val2)


VALID_CFG_PARAM_NAMES = {
    'addform_entry_templates': dict,
    'addform_parent_attrs': tuple,
    'binddn_mapping': str,
    'boundas_template': dict,
    'bulkmod_delold': bool,
    'description': str,
    'dit_max_levels': int,
    'dit_search_sizelimit': int,
    'dit_search_timelimit': int,
    'groupadm_defs': dict,
    'groupadm_filterstr_template': str,
    'groupadm_optgroup_bounds': tuple,
    'inputform_supentrytemplate': dict,
    'input_template': dict,
    'login_template': str,
    'modify_constant_attrs': tuple,
    'naming_contexts': tuple,
    'passwd_genchars': str,
    'passwd_genlength': int,
    'passwd_hashtypes': tuple,
    'passwd_modlist': tuple,
    'passwd_template': str,
    'print_cols': int,
    'print_template': dict,
    'read_tablemaxcount': dict,
    'read_template': dict,
    'rename_supsearchurl': dict,
    'rename_template': str,
    'requested_attrs': tuple,
    '_schema': None,
    'schema_supplement': str,
    'schema_strictcheck': int,
    'schema_uri': str,
    'search_attrs': tuple,
    'searchform_search_root_url': str,
    'searchform_template': dict,
    'searchoptions_template': str,
    'search_resultsperpage': int,
    'search_tdtemplate': dict,
    'session_track_control': bool,
    'starttls': int,
    'supplement_schema': str,
    'timeout': int,
    'tls_options': dict,
    'top_template': str,
    'vcard_template': dict,
}


class Web2LDAPConfig(LogHelper):
    """
    Base class for a web2ldap host-/backend configuration section.
    """
    __slots__ = tuple(VALID_CFG_PARAM_NAMES.keys())

    def __init__(self, **params):
        self.update(params)

    def update(self, params):
        """
        sets params as class attributes
        """
        for param_name, param_val in params.items():
#            self.log(logging.DEBUG, 'update() %r // %r', param_name, param_val)
            try:
                param_type = VALID_CFG_PARAM_NAMES[param_name]
            except KeyError:
                raise ValueError('Invalid config parameter %r.' % (param_name))
            if param_type is not None and not isinstance(param_val, param_type):
                raise TypeError(
                    'Invalid type for config parameter %r. Expected %r, got %r' % (
                        param_name,
                        param_type,
                        param_val,
                    )
                )
            setattr(self, param_name, param_val)

    def clone(self, **params):
        """
        returns a copy of the current Web2LDAPConfig
        with some more params set
        """
        old_params = {
            param_name: getattr(self, param_name)
            for param_name in VALID_CFG_PARAM_NAMES
            if hasattr(self, param_name)
        }
        new = Web2LDAPConfig(**old_params)
        new.update(params)
        self.log(
            logging.DEBUG,
            'Cloned config %s with %d parameters to %s with %d new params %s',
            id(self),
            len(old_params),
            id(new),
            len(params),
            params,
        )
        return new
