# -*- coding: ascii -*-
"""
web2ldap plugin classes for schema elements defined in RFC2307
"""

import re
from typing import Dict

from ...web.forms import Field
from ..searchform import SEARCH_OPT_IS_EQUAL
from ..schema.syntaxes import (
    DaysSinceEpoch,
    DNSDomain,
    DynamicValueSelectList,
    IA5String,
    Integer,
    IPHostAddress,
    IPServicePortNumber,
    MacAddress,
    SelectList,
    syntax_registry,
)


class RFC2307BootParameter(IA5String):
    oid: str = '1.3.6.1.1.1.0.1'
    desc: str = 'RFC2307 Boot Parameter'
    pattern = None # just a stub, should be made stricter


class GidNumber(DynamicValueSelectList, Integer):
    oid: str = 'GidNumber-oid'
    desc: str = 'RFC2307: An integer uniquely identifying a group in an administrative domain'
    min_value = 0
    max_value = 4294967295
    ldap_url = 'ldap:///_?gidNumber,cn?sub?(objectClass=posixGroup)'

    def _validate(self, attr_value: bytes) -> bool:
        return Integer._validate(self, attr_value)

    def display(self, vidx, links) -> str:
        # Possibly display a link
        ocs = self._entry.object_class_oid_set()
        if 'posixAccount' in ocs or 'shadowAccount' in ocs:
            return DynamicValueSelectList.display(self, vidx, links)
        res = [Integer.display(self, vidx, False)]
        if not links:
            return res[0]
        if 'posixGroup' in ocs:
            title = 'Search primary group members'
            searchform_params = [
                ('dn', self._dn),
                ('searchform_mode', 'adv'),
                ('search_attr', 'objectClass'),
                ('search_option', SEARCH_OPT_IS_EQUAL),
                ('search_string', 'posixAccount'),
                ('search_attr', 'gidNumber'),
                ('search_option', SEARCH_OPT_IS_EQUAL),
                ('search_string', self.av_u),
            ]
        else:
            title = None
            searchform_params = None
        if title and searchform_params:
            res.append(self._app.anchor(
                'searchform', '&raquo;',
                searchform_params,
                title=title,
            ))
        return ' '.join(res)

    def input_field(self) -> Field:
        ocs = self._entry.object_class_oid_set()
        if 'posixAccount' in ocs or 'shadowAccount' in ocs:
            return DynamicValueSelectList.input_field(self)
        return Integer.input_field(self)

syntax_registry.reg_at(
    GidNumber.oid, [
        '1.3.6.1.1.1.1.1', # gidNumber
    ]
)


class MemberUID(IA5String, DynamicValueSelectList):
    oid: str = 'MemberUID-oid'
    desc: str = 'RFC2307 numerical UID of group member(s)'
    ldap_url = None
    #ldap_url = 'ldap:///_?uid,cn?sub?(objectClass=posixAccount)'

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attr_value, entry)
        if self.ldap_url:
            DynamicValueSelectList.__init__(self, app, dn, schema, attrType, attr_value, entry)

    def _validate(self, attr_value: bytes) -> bool:
        if self.ldap_url:
            return DynamicValueSelectList._validate(self, attr_value)
        return IA5String._validate(self, attr_value)

    def input_field(self) -> Field:
        if self.ldap_url:
            return DynamicValueSelectList.input_field(self)
        return IA5String.input_field(self)

    def display(self, vidx, links) -> str:
        res = [IA5String.display(self, vidx, False)]
        if links:
            res.append(self._app.anchor(
                'searchform', '&raquo;',
                [
                    ('dn', self._dn),
                    (
                        'filterstr', '(&(objectClass=posixAccount)(uid=%s))' % (
                            self._app.form.s2d(self.av_u)
                        )
                    ),
                    ('searchform_mode', 'exp'),
                ],
                title='Search for user entry',
            ))
        return ' '.join(res)

syntax_registry.reg_at(
    MemberUID.oid, [
        '1.3.6.1.1.1.1.12', # memberUid
    ]
)


class RFC2307NISNetgroupTriple(IA5String):
    oid: str = '1.3.6.1.1.1.0.0'
    desc: str = 'RFC2307 NIS Netgroup Triple'
    pattern = re.compile(r'^\([a-z0-9.-]*,[a-z0-9.-]*,[a-z0-9.-]*\)$')


class UidNumber(Integer):
    oid: str = 'UidNumber-oid'
    desc: str = 'Numerical user ID for Posix systems'
    min_value = 0
    max_value = 4294967295

syntax_registry.reg_at(
    UidNumber.oid, [
        '1.3.6.1.1.1.1.0', # uidNumber
    ]
)


class Shell(SelectList):
    oid: str = 'Shell-oid'
    desc: str = 'Shell for user of Posix systems'
    attr_value_dict: Dict[str, str] = {
        '/bin/sh': 'Standard shell /bin/sh',
        '/bin/bash': 'Bourne-Again SHell /bin/bash',
        '/bin/csh': '/bin/csh',
        '/bin/tcsh': '/bin/tcsh',
        '/bin/ksh': 'Korn shell /bin/ksh',
        '/bin/passwd': 'Password change /bin/passwd',
        '/bin/true': '/bin/true',
        '/bin/false': '/bin/false',
        '/bin/zsh': 'Zsh /bin/zsh',
        '/usr/bin/bash': 'Bourne-Again SHell /usr/bin/bash',
        '/usr/bin/csh': '/usr/bin/csh',
        '/usr/bin/tcsh': '/usr/bin/csh',
        '/usr/bin/ksh': 'Korn shell /usr/bin/ksh',
        '/usr/bin/zsh': 'Zsh /usr/bin/zsh',
        '/usr/sbin/nologin': 'Login denied /usr/sbin/nologin',
    }

syntax_registry.reg_at(
    Shell.oid, [
        '1.3.6.1.1.1.1.4', # loginShell
    ]
)


class IpServiceProtocol(SelectList):
    oid: str = 'IpServiceProtocol-oid'
    desc: str = 'RFC 2307: IP service protocol'

    attr_value_dict: Dict[str, str] = {
        'tcp': 'tcp',
        'udp': 'udp',
    }

syntax_registry.reg_at(
    IpServiceProtocol.oid, [
        '1.3.6.1.1.1.1.16', # ipServiceProtocol
    ]
)


syntax_registry.reg_at(
    IPHostAddress.oid, [
        '1.3.6.1.1.1.1.19', # ipHostNumber
        '1.3.6.1.1.1.1.20', # ipNetworkNumber
    ]
)


syntax_registry.reg_at(
    DNSDomain.oid, [
        '1.3.6.1.1.1.1.30', # nisDomain
    ]
)


syntax_registry.reg_at(
    DaysSinceEpoch.oid, [
        '1.3.6.1.1.1.1.10', # shadowExpire
        '1.3.6.1.1.1.1.5', # shadowLastChange
    ]
)


syntax_registry.reg_at(
    IPServicePortNumber.oid, [
        '1.3.6.1.1.1.1.15', # ipServicePort
    ]
)


syntax_registry.reg_at(
    MacAddress.oid, [
        '1.3.6.1.1.1.1.22', # macAddress
    ]
)


# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
