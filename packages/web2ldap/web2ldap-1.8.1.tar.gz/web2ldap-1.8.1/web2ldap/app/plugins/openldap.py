# -*- coding: ascii -*-
"""
web2ldap plugin classes for OpenLDAP
"""

import re
import binascii
from typing import Dict

from pyasn1.codec.ber import decoder as ber_decoder

import ldap0.ldapurl
import ldap0.controls
import ldap0.openldap
from ldap0.controls import KNOWN_RESPONSE_CONTROLS

import web2ldapcnf

from ..searchform import SEARCH_OPT_IS_EQUAL, SEARCH_SCOPE_STR_ONELEVEL
from ..schema.syntaxes import (
    AuthzDN,
    BindDN,
    DirectoryString,
    DistinguishedName,
    DynamicDNSelectList,
    IA5String,
    Integer,
    LDAPUrl,
    LDAPv3ResultCode,
    MultilineText,
    NotBefore,
    OctetString,
    SchemaDescription,
    SelectList,
    Uri,
    UUID,
    syntax_registry,
)
from ...ldaputil.oidreg import OID_REG
from .quirks import NamingContexts

#---------------------------------------------------------------------------
# Schema information
#---------------------------------------------------------------------------

class OlcSchemaDescription(SchemaDescription):
    oid: str = 'OlcSchemaDescription-oid'

    def _validate(self, attr_value: bytes) -> bool:
        try:
            # strip X-ORDERED number
            schema_desc = attr_value.split(b'}', 1)[1]
        except IndexError:
            schema_desc = attr_value
        return SchemaDescription._validate(self, schema_desc)


class OlcObjectClasses(OlcSchemaDescription):
    oid: str = 'OlcObjectClasses-oid'
    schema_cls = ldap0.schema.models.ObjectClass

syntax_registry.reg_at(
    OlcObjectClasses.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.0.32', # olcObjectClasses
    ]
)


class OlcAttributeTypes(OlcSchemaDescription):
    oid: str = 'OlcAttributeTypes-oid'
    schema_cls = ldap0.schema.models.AttributeType

syntax_registry.reg_at(
    OlcAttributeTypes.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.0.4', # olcAttributeTypes
    ]
)


class OlcLdapSyntaxes(OlcSchemaDescription):
    oid: str = 'OlcLdapSyntaxes-oid'
    schema_cls = ldap0.schema.models.LDAPSyntax

syntax_registry.reg_at(
    OlcLdapSyntaxes.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.0.85', # olcLdapSyntaxes
    ]
)


class OlcDitContentRules(OlcSchemaDescription):
    oid: str = 'OlcDitContentRules-oid'
    schema_cls = ldap0.schema.models.DITContentRule

syntax_registry.reg_at(
    OlcDitContentRules.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.0.16', # olcDitContentRules
    ]
)

#---------------------------------------------------------------------------
# slapo-syncprov
#---------------------------------------------------------------------------

# see https://www.openldap.org/faq/data/cache/1145.html
class CSNSid(IA5String):
    oid: str = '1.3.6.1.4.1.4203.666.11.2.4'
    desc: str = 'change sequence number SID (CSN SID)'
    min_len: int = 3
    max_len: int = 3
    pattern = re.compile('^[a-fA-F0-9]{3}$')


# see https://www.openldap.org/faq/data/cache/1145.html
class CSN(IA5String):
    oid: str = '1.3.6.1.4.1.4203.666.11.2.1'
    desc: str = 'change sequence number (CSN)'
    min_len: int = 40
    max_len: int = 40
    pattern = re.compile('^[0-9]{14}\\.[0-9]{6}Z#[a-fA-F0-9]{6}#[a-fA-F0-9]{3}#[a-fA-F0-9]{6}$')

syntax_registry.reg_at(
    CSN.oid, [
        '1.3.6.1.4.1.4203.666.1.25', # contextCSN
        '1.3.6.1.4.1.4203.666.1.7',  # entryCSN
        '1.3.6.1.4.1.4203.666.1.13', # namingCSN
        # also register by name in case OpenLDAP was built without -DSLAP_SCHEMA_EXPOSE
        'contextCSN', 'entryCSN', 'namingCSN',
    ]
)

#---------------------------------------------------------------------------
# back-config
#---------------------------------------------------------------------------

syntax_registry.reg_at(
    NamingContexts.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.10', # olcSuffix
    ]
)


class OlcDbIndex(DirectoryString):
    oid: str = 'OlcDbIndex-oid'
    desc: str = 'OpenLDAP indexing directive'
    pattern = re.compile("^[a-zA-Z]?[a-zA-Z0-9.,;-]* (pres|eq|sub)(,(pres|eq|sub))*$")

syntax_registry.reg_at(
    OlcDbIndex.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.2', # olcDbIndex
    ]
)


class OlcSubordinate(SelectList):
    oid: str = 'OlcSubordinate-oid'
    desc: str = 'Indicates whether backend is subordinate'
    attr_value_dict: Dict[str, str] = {
        '': '-/- (FALSE)',
        'TRUE': 'TRUE',
        'advertise': 'advertise',
    }

syntax_registry.reg_at(
    OlcSubordinate.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.15', # olcSubordinate
    ]
)


class OlcRootDN(BindDN):
    oid: str = 'OlcRootDN-oid'
    desc: str = 'The rootdn in the database'
    default_rdn = 'cn=admin'

    def form_value(self) -> str:
        fval = BindDN.form_value(self)
        try:
            olc_suffix = self._entry['olcSuffix'][0].decode()
        except KeyError:
            pass
        else:
            if not fval or not fval.endswith(olc_suffix):
                try:
                    fval = ','.join((self.default_rdn, olc_suffix))
                except KeyError:
                    pass
        return fval

syntax_registry.reg_at(
    OlcRootDN.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.8', # olcRootDN
    ]
)


class OlcMultilineText(MultilineText):
    oid: str = 'OlcMultilineText-oid'
    desc: str = 'OpenLDAP multiline configuration strings'
    cols = 90
    min_input_rows = 3

    def display(self, vidx, links) -> str:
        return '<code>%s</code>' % MultilineText.display(self, vidx, links)

syntax_registry.reg_at(
    OlcMultilineText.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.0.1', # olcAccess
        '1.3.6.1.4.1.4203.1.12.2.3.0.6', # olcAuthIDRewrite
        '1.3.6.1.4.1.4203.1.12.2.3.0.8', # olcAuthzRegexp
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.5', # olcLimits
    ]
)

class OlcSyncRepl(OlcMultilineText, LDAPUrl):
    oid: str = 'OlcSyncRepl-oid'
    desc: str = 'OpenLDAP syncrepl directive'
    min_input_rows = 5

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        OlcMultilineText.__init__(self, app, dn, schema, attrType, attr_value, entry)

    def display(self, vidx, links) -> str:
        if not links or not self._av:
            return OlcMultilineText.display(self, vidx, links)
        srd = ldap0.openldap.SyncReplDesc(self.av_u)
        return ' '.join((
            OlcMultilineText.display(self, vidx, links),
            self._app.ldap_url_anchor(srd.ldap_url()),
        ))

syntax_registry.reg_at(
    OlcSyncRepl.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.2.0.11', # olcSyncrepl
    ]
)


class OlmSeeAlso(DynamicDNSelectList):
    oid: str = 'OlmSeeAlso-oid'
    desc: str = 'DN of a overlase or database object in back-monitor'
    ldap_url = (
        'ldap:///_?monitoredInfo?sub?'
        '(&'
        '(objectClass=monitoredObject)'
        '(|'
        '(entryDN:dnOneLevelMatch:=cn=Databases,cn=Monitor)'
        '(entryDN:dnOneLevelMatch:=cn=Overlays,cn=Monitor)'
        '(entryDN:dnOneLevelMatch:=cn=Backends,cn=Monitor)'
        ')'
        ')'
    )

syntax_registry.reg_at(
    OlmSeeAlso.oid, [
        '2.5.4.34', # seeAlso
    ],
    structural_oc_oids=['1.3.6.1.4.1.4203.666.3.16.8'], # monitoredObject
)


class OlcPPolicyDefault(DistinguishedName):
    oid: str = 'OlcPPolicyDefault-oid'
    desc: str = 'DN of a pwdPolicy object for uncustomized objects'

syntax_registry.reg_at(
    OlcPPolicyDefault.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.3.12.1', # olcPPolicyDefault
    ]
)


class OlcMemberOfDangling(SelectList):
    oid: str = 'OlcMemberOfDangling-oid'
    desc: str = 'Behavior in case of dangling references during modification'
    attr_value_dict: Dict[str, str] = {
        '': '-/-',
        'ignore': 'ignore',
        'drop': 'drop',
        'error': 'error',
    }

syntax_registry.reg_at(
    OlcMemberOfDangling.oid, [
        '1.3.6.1.4.1.4203.1.12.2.3.3.18.1', # olcMemberOfDangling
    ]
)


#---------------------------------------------------------------------------
# slapo-accesslog
#---------------------------------------------------------------------------


syntax_registry.reg_at(
    NotBefore.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.2', 'reqStart',
        '1.3.6.1.4.1.4203.666.11.5.1.3', 'reqEnd',
    ]
)


class AuditContext(NamingContexts):
    oid: str = 'AuditContext'
    desc: str = 'OpenLDAP DN pointing to audit naming context'

    def display(self, vidx, links) -> str:
        res = [DistinguishedName.display(self, vidx, links)]
        if links:
            res.extend([
                self._app.anchor(
                    'searchform', 'Search',
                    [
                        ('dn', self.av_u),
                        ('scope', str(ldap0.SCOPE_ONELEVEL)),
                    ],
                    title='Go to search form for audit log',
                ),
                self._app.anchor(
                    'search', 'List all',
                    [
                        ('dn', self.av_u),
                        ('filterstr', '(objectClass=auditObject)'),
                        ('scope', str(ldap0.SCOPE_ONELEVEL)),
                    ],
                    title='List audit log entries of all operations',
                ),
                self._app.anchor(
                    'search', 'List writes',
                    [
                        ('dn', self.av_u),
                        ('filterstr', '(objectClass=auditWriteObject)'),
                        ('scope', str(ldap0.SCOPE_ONELEVEL)),
                    ],
                    title='List audit log entries of all write operations',
                ),
            ])
        return web2ldapcnf.command_link_separator.join(res)

syntax_registry.reg_at(
    AuditContext.oid,
    [
        '1.3.6.1.4.1.4203.666.11.5.1.30', 'auditContext',
        '1.3.6.1.4.1.4203.1.12.2.3.3.4.1',  # olcAccessLogDB
    ]
)


class ReqResult(LDAPv3ResultCode):
    oid: str = 'ReqResult-oid'

syntax_registry.reg_at(
    ReqResult.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.7', 'reqResult', # reqResult
    ]
)


class ReqMod(OctetString, DirectoryString):
    oid: str = 'ReqMod-oid'
    desc: str = 'List of modifications/old values'
    known_modtypes = {b'+', b'-', b'=', b'#', b''}

    def _validate(self, attr_value: bytes) -> bool:
        return OctetString._validate(self, attr_value)

    def display(self, vidx, links) -> str:
        if self._av == b':':
            # magic value used for fixing OpenLDAP ITS#6545
            return ':'
        try:
            mod_attr_type, mod_attr_rest = self._av.split(b':', 1)
            mod_type = mod_attr_rest[0:1].strip()
        except (ValueError, IndexError):
            return OctetString.display(self, vidx, links)
        if not mod_type in self.known_modtypes:
            return OctetString.display(self, vidx, links)
        if len(mod_attr_rest) > 1:
            try:
                mod_type, mod_attr_value = mod_attr_rest.split(b' ', 1)
            except ValueError:
                return OctetString.display(self, vidx, links)
        else:
            mod_attr_value = b''
        mod_attr_type_u = mod_attr_type.decode(self._app.ls.charset)
        mod_type_u = mod_type.decode(self._app.ls.charset)
        try:
            mod_attr_value.decode(self._app.ls.charset)
        except UnicodeDecodeError:
            return '%s:%s<br>\n<code>\n%s\n</code>\n' % (
                self._app.form.s2d(mod_attr_type_u),
                self._app.form.s2d(mod_type_u),
                mod_attr_value.hex().upper(),
            )
        else:
            return DirectoryString.display(self, vidx, links)
        raise ValueError

syntax_registry.reg_at(
    ReqMod.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.16', 'reqMod',
        '1.3.6.1.4.1.4203.666.11.5.1.17', 'reqOld',
    ]
)


class ReqControls(IA5String):
    oid: str = '1.3.6.1.4.1.4203.666.11.5.3.1'
    desc: str = 'List of LDAPv3 extended controls sent along with a request'

    def display(self, vidx, links) -> str:
        result_lines = [IA5String.display(self, vidx, links)]
        # Eliminate X-ORDERED prefix
        _, rest = self.av_u.strip().split('}{', 1)
        # check whether it ends with }
        if rest.endswith('}'):
            result_lines.append('Extracted:')
            # consume } and split tokens
            ctrl_tokens = list(filter(
                None,
                [t.strip() for t in rest[:-1].split(' ')]
            ))
            ctrl_type = ctrl_tokens[0]
            try:
                ctrl_name, _, _ = OID_REG[ctrl_type]
            except (KeyError, ValueError):
                try:
                    ctrl_name = KNOWN_RESPONSE_CONTROLS.get(ctrl_type).__class__.__name__
                except KeyError:
                    ctrl_name = None
            if ctrl_name:
                result_lines.append(self._app.form.s2d(ctrl_name))
            # Extract criticality
            try:
                ctrl_criticality = {
                    'TRUE': True,
                    'FALSE': False,
                }[ctrl_tokens[ctrl_tokens.index('criticality')+1].upper()]
            except (KeyError, ValueError, IndexError):
                ctrl_criticality = False
            result_lines.append('criticality %s' % str(ctrl_criticality).upper())
            # Extract controlValue
            try:
                ctrl_value = binascii.unhexlify(
                    ctrl_tokens[ctrl_tokens.index('controlValue')+1].upper()[1:-1]
                )
            except (KeyError, ValueError, IndexError):
                pass
            else:
                try:
                    decoded_control_value = ber_decoder.decode(ctrl_value)
                except Exception:
                    decoded_control_value = ctrl_value
                result_lines.append(
                    'controlValue %s' % (
                        self._app.form.s2d(
                            repr(decoded_control_value)
                        ).replace('\n', '<br>')
                    )
                )
        return '<br>'.join(result_lines)

syntax_registry.reg_at(
    ReqControls.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.10', 'reqControls',
        '1.3.6.1.4.1.4203.666.11.5.1.11', 'reqRespControls',
    ]
)


class ReqEntryUUID(UUID):
    oid: str = 'ReqEntryUUID-oid'

    def display(self, vidx, links) -> str:
        display_value = UUID.display(self, vidx, links)
        if not links:
            return display_value
        return web2ldapcnf.command_link_separator.join((
            display_value,
            self._app.anchor(
                'search', 'Search target',
                (
                    ('dn', self._dn),
                    (
                        'filterstr',
                        '(entryUUID=%s)' % (self.av_u),
                    ),
                    (
                        'search_root',
                        str(
                            self._app.ls.get_search_root(
                                self._entry['reqDN'][0].decode(self._app.ls.charset)
                            )
                        ),
                    ),
                ),
                title='Search entry by UUID',
            )
        ))

syntax_registry.reg_at(
    ReqEntryUUID.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.31', 'reqEntryUUID', # reqEntryUUID
    ]
)


class ReqSession(Integer):
    oid: str = 'ReqSession-oid'

    def display(self, vidx, links) -> str:
        display_value = Integer.display(self, vidx, links)
        if not links:
            return display_value
        return web2ldapcnf.command_link_separator.join((
            display_value,
            self._app.anchor(
                'search', '&raquo;',
                (
                    ('dn', self._dn),
                    ('search_root', str(self._app.naming_context)),
                    ('searchform_mode', 'adv'),
                    ('search_attr', 'reqSession'),
                    ('search_option', SEARCH_OPT_IS_EQUAL),
                    ('search_string', self.av_u),
                ),
                title='Search all audit entries with same session number',
            )
        ))

syntax_registry.reg_at(
    ReqSession.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.5', 'reqSession', # reqSession
    ]
)


class ReqDN(DistinguishedName):
    oid: str = 'ReqDN-oid'
    desc: str = 'Target DN of request'
    ref_attrs = (
        ('reqDN', 'Same target', None, 'Search all entries with same target DN'),
    )


syntax_registry.reg_at(
    ReqDN.oid, [
        '1.3.6.1.4.1.4203.666.11.5.1.1', 'reqDN', # reqDN
    ]
)


class ReqAuthzID(DistinguishedName):
    oid: str = 'ReqAuthzID-oid'
    desc: str = 'Authorization DN'
    ref_attrs = (
        ('reqAuthzID', 'Same authz-DN', None, 'Search all entries with same authz DN'),
    )


syntax_registry.reg_at(
    ReqAuthzID.oid, [
        'reqAuthzID',
        '1.3.6.1.4.1.4203.666.11.5.1.6', # reqAuthzID
    ]
)


#---------------------------------------------------------------------------
# General
#---------------------------------------------------------------------------


class Authz(DirectoryString):
    oid: str = '1.3.6.1.4.1.4203.666.2.7'
    desc: str = 'OpenLDAP authz'


syntax_registry.reg_at(
    AuthzDN.oid, [
        'monitorConnectionAuthzDN',
        '1.3.6.1.4.1.4203.666.1.55.7', # monitorConnectionAuthzDN
    ]
)


class OpenLDAPACI(DirectoryString):
    oid: str = '1.3.6.1.4.1.4203.666.2.1'
    desc: str = 'OpenLDAP ACI'


class OpenLDAPSpecialBackendSuffix(NamingContexts):
    oid: str = 'OpenLDAPSpecialBackendSuffix-oid'
    desc: str = 'OpenLDAP special backend suffix'

    def _config_link(self):
        attr_type_u = self._at[:-7]
        try:
            config_context = self._app.ls.root_dse['configContext'][0].decode(self._app.ls.charset)
        except KeyError:
            return None
        return self._app.anchor(
            'search', 'Config',
            (
                ('dn', config_context),
                ('scope', SEARCH_SCOPE_STR_ONELEVEL),
                (
                    'filterstr',
                    '(&(objectClass=olcDatabaseConfig)(olcDatabase=%s))' % (attr_type_u),
                ),
            ),
            title='Search for configuration entry below %s' % (config_context),
        )

syntax_registry.reg_at(
    OpenLDAPSpecialBackendSuffix.oid,
    [
        'monitorContext', '1.3.6.1.4.1.4203.666.1.10',
        'configContext', '1.3.6.1.4.1.4203.1.12.2.1',
    ]
)


syntax_registry.reg_at(
    Uri.oid, ['monitorConnectionListener']
)


syntax_registry.reg_at(
    DistinguishedName.oid, [
        'entryDN',
    ]
)

# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
