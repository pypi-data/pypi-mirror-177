# -*- coding: ascii -*-
"""
web2ldap plugin classes for attributes defined for so-called dynamic groups
"""

import ldap0
import ldap0.ldapurl
from ldap0.dn import is_dn

from ..schema.syntaxes import LDAPUrl, syntax_registry


class MemberUrl(LDAPUrl):
    """
    Plugin class for attribute memberUrl which contains an LDAP URI
    specifying the group members.
    """
    oid: str = 'MemberUrl-oid'
    desc: str = 'LDAP URL describing search parameters used to lookup group members'
    ldap_url = None

    def _validate(self, attr_value: bytes) -> bool:
        """
        Checks validity of membership LDAP URL.
        False if hostport part is non-empty, the search base is not a valid DN,
        or the base search to search base failed.
        """
        try:
            ldap_url = ldap0.ldapurl.LDAPUrl(attr_value.decode(self._app.ls.charset))
        except ValueError:
            return False
        search_base = ldap_url.dn
        if not is_dn(search_base) or ldap_url.hostport:
            return False
        try:
            # Try a dummy base-levelsearch with search base and filter string
            # to provoke server-side errors
            self._app.ls.l.read_s(
                ldap_url.dn,
                attrlist=ldap_url.attrs,
                filterstr=ldap_url.filterstr or '(objectClass=*)',
            )
        except ldap0.LDAPError:
            return False
        return True


syntax_registry.reg_at(
    MemberUrl.oid, [
        '2.16.840.1.113730.3.1.198', # memberUrl
    ]
)


# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
