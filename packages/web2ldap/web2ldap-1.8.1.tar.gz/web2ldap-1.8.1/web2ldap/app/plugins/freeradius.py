# -*- coding: ascii -*-
"""
web2ldap plugin classes for FreeRADIUS/LDAP schema

See also:
https://github.com/FreeRADIUS/freeradius-server/tree/master/doc/schemas/ldap/openldap
"""

from ..schema.syntaxes import DynamicDNSelectList, syntax_registry


class RadiusProfileDN(DynamicDNSelectList):
    """
    Select plugin for choosing DN where rlm_ldap should find the
    RADIUS profile associated with an entry
    """
    oid: str = 'RadiusProfileDN-oid'
    desc: str = 'DN of a radius profile entry with real data'
    ldap_url = 'ldap:///_??sub?(&(objectClass=radiusprofile)(!(radiusProfileDn=*)))'

syntax_registry.reg_at(
    RadiusProfileDN.oid, [
        '1.3.6.1.4.1.3317.4.3.1.49', # radiusProfileDn
    ]
)


# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
