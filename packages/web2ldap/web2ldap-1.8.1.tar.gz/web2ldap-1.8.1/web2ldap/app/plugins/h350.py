# -*- coding: ascii -*-
"""
web2ldap plugin classes for H.350 Directory Services (see RFC 3944)
"""

from ..schema.syntaxes import Uri, LDAPUrl, syntax_registry


class CommURI(LDAPUrl):
    oid: str = 'CommURI-oid'
    desc: str = 'Labeled URI format to point to the distinguished name of the commUniqueId'

syntax_registry.reg_at(
    CommURI.oid, [
        '0.0.8.350.1.1.1.1.1', # commURI
        '0.0.8.350.1.1.2.1.2', # commOwner
    ]
)


syntax_registry.reg_at(
    Uri.oid, [
        '0.0.8.350.1.1.6.1.1', # SIPIdentitySIPURI
    ]
)


# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
