# -*- coding: ascii -*-
"""
web2ldap plugin classes for attributes defined in draft-vchu-ldap-pwd-policy
"""

from typing import Dict

from ..schema.syntaxes import SelectList, syntax_registry


class OnOffFlag(SelectList):
    """
    Plugin class for flag attribute with value "on" or "off"
    """
    oid: str = 'OnOffFlag-oid'
    desc: str = 'Only values "on" or "off" are allowed'
    attr_value_dict: Dict[str, str] = {
        'on': 'on',
        'off': 'off',
    }

syntax_registry.reg_at(
    OnOffFlag.oid, [
        '2.16.840.1.113730.3.1.102', # passwordChange, pwdAllowUserChange
        '2.16.840.1.113730.3.1.103', # passwordCheckSyntax, pwdCheckSyntax
        '2.16.840.1.113730.3.1.98',  # passwordExp
        '2.16.840.1.113730.3.1.105', # passwordLockout, pwdLockOut
        '2.16.840.1.113730.3.1.220', # passwordMustChange, pwdMustChange
        '2.16.840.1.113730.3.1.108', # passwordUnlock
    ]
)


# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
