# -*- coding: ascii -*-
"""
web2ldap.app.schema.syntaxes: classes for known attribute types

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import binascii
import sys
import re
import imghdr
import sndhdr
import urllib.parse
import uuid
import datetime
import time
import json
import inspect
import warnings
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    Union,
)
import ipaddress
from collections import defaultdict
from io import BytesIO

import iso3166

try:
    import defusedxml.ElementTree
except ImportError:
    DEFUSEDXML_AVAIL = False
else:
    DEFUSEDXML_AVAIL = True

try:
    import phonenumbers
except ImportError:
    PHONENUMBERS_AVAIL = False
else:
    PHONENUMBERS_AVAIL = True

# Detect Python Imaging Library (PIL)
try:
    from PIL import Image as PILImage
except ImportError:
    PIL_AVAIL = False
else:
    PIL_AVAIL = True
    warnings.simplefilter('error', PILImage.DecompressionBombWarning)

import ldap0
import ldap0.ldapurl
from ldap0.schema.models import AttributeType, ObjectClass, OBJECTCLASS_KIND_STR
from ldap0.controls.deref import DereferenceControl
from ldap0.dn import DNObj, is_dn
from ldap0.res import SearchResultEntry
from ldap0.schema.subentry import SubSchema

import web2ldapcnf

from ...web import forms as web_forms
from ...msbase import ascii_dump, chunks
from ...utctime import repr2ts, ts2repr, strftimeiso8601
from ...ldaputil.oidreg import OID_REG
from ...log import logger
from ... import cmp
from . import schema_anchor
from ..tmpl import get_variant_filename
from ...utctime import strptime as utc_strptime
from ..searchform import (
    SEARCH_OPT_ATTR_EXISTS,
    SEARCH_OPT_IS_EQUAL,
    SEARCH_SCOPE_STR_ONELEVEL,
)


class SyntaxRegistry:
    """
    syntax registry used to register plugin classes
    """
    __slots__ = (
        'at2syntax',
        'oid2syntax',
    )

    def __init__(self):
        self.oid2syntax = ldap0.cidict.CIDict()
        self.at2syntax = defaultdict(dict)

    def reg_syntax(self, cls):
        """
        register a syntax classes for an OID
        """
        assert isinstance(cls.oid, str), ValueError(
            'Expected %s.oid to be str, got %r' % (cls.__name__, cls.oid,)
        )
        logger.debug('Register syntax class %r with OID %r', cls.__name__, cls.oid)
        # FIX ME!
        # A better approach for unique syntax plugin class registration which
        # allows overriding older registration is needed.
        if cls.oid in self.oid2syntax and cls != self.oid2syntax[cls.oid]:
            raise ValueError(
                (
                    'Failed to register syntax class %s.%s with OID %s,'
                    ' already registered by %s.%s'
                ) % (
                    cls.__module__,
                    cls.__name__,
                    repr(cls.oid),
                    self.oid2syntax[cls.oid].__module__,
                    self.oid2syntax[cls.oid].__name__,
                )
            )
        self.oid2syntax[cls.oid] = cls

    def reg_syntaxes(self, modulename):
        """
        register all syntax classes found in given module
        """
        logger.debug('Register syntax classes from module %r', modulename)
        for _, cls in inspect.getmembers(sys.modules[modulename], inspect.isclass):
            if issubclass(cls, LDAPSyntax) and hasattr(cls, 'oid'):
                self.reg_syntax(cls)

    def reg_at(self, syntax_oid: str, attr_types, structural_oc_oids=None):
        """
        register an attribute type (by OID) to explicitly use a certain LDAPSyntax class
        """
        logger.debug(
            'Register syntax OID %s for %r / %r',
            syntax_oid,
            attr_types,
            structural_oc_oids,
        )
        assert isinstance(syntax_oid, str), ValueError(
            'Expected syntax_oid to be str, got %r' % (syntax_oid,)
        )
        structural_oc_oids = list(filter(None, map(str.strip, structural_oc_oids or []))) or [None]
        for atype in attr_types:
            atype = atype.strip()
            for oc_oid in structural_oc_oids:
                # FIX ME!
                # A better approach for unique attribute type registration which
                # allows overriding older registration is needed.
                if atype in self.at2syntax and oc_oid in self.at2syntax[atype]:
                    logger.warning(
                        (
                            'Registering attribute type %r with syntax %r'
                            ' overrides existing registration with syntax %r'
                        ),
                        atype,
                        syntax_oid,
                        self.at2syntax[atype],
                    )
                self.at2syntax[atype][oc_oid] = syntax_oid

    def get_syntax(self, schema, attrtype_nameoroid, structural_oc):
        """
        returns LDAPSyntax class for given attribute type
        """
        assert isinstance(attrtype_nameoroid, str), ValueError(
            'Expected attrtype_nameoroid to be str, got %r' % (attrtype_nameoroid,)
        )
        assert structural_oc is None or isinstance(structural_oc, str), ValueError(
            'Expected structural_oc to be str or None, got %r' % (structural_oc,)
        )
        attrtype_oid = schema.get_oid(AttributeType, attrtype_nameoroid)
        if structural_oc:
            structural_oc_oid = schema.get_oid(ObjectClass, structural_oc)
        else:
            structural_oc_oid = None
        syntax_oid = LDAPSyntax.oid
        try:
            syntax_oid = self.at2syntax[attrtype_oid][structural_oc_oid]
        except KeyError:
            try:
                syntax_oid = self.at2syntax[attrtype_oid][None]
            except KeyError:
                attrtype_se = schema.get_inheritedobj(
                    AttributeType,
                    attrtype_oid,
                    ['syntax'],
                )
                if attrtype_se and attrtype_se.syntax:
                    syntax_oid = attrtype_se.syntax
        try:
            syntax_class = self.oid2syntax[syntax_oid]
        except KeyError:
            syntax_class = LDAPSyntax
        return syntax_class

    def get_at(self, app, dn, schema, attr_type, attr_value, entry=None):
        """
        returns LDAPSyntax instance fully initialized for given attribute
        """
        if entry:
            structural_oc = entry.get_structural_oc()
        else:
            structural_oc = None
        syntax_class = self.get_syntax(schema, attr_type, structural_oc)
        attr_instance = syntax_class(app, dn, schema, attr_type, attr_value, entry)
        return attr_instance

    def check(self):
        """
        check whether attribute registry dict contains references by OID
        for which no LDAPSyntax class are registered
        """
        logger.debug(
            'Checking %d LDAPSyntax classes and %d attribute type mappings',
            len(self.oid2syntax),
            len(self.at2syntax),
        )
        for atype in self.at2syntax:
            for object_class in self.at2syntax[atype]:
                if self.at2syntax[atype][object_class] not in self.oid2syntax:
                    logger.warning('No LDAPSyntax registered for (%r, %r)', atype, object_class)


####################################################################
# Classes of known syntaxes
####################################################################


class LDAPSyntaxValueError(ValueError):
    """
    Exception raised in case a syntax check failed
    """


class LDAPSyntaxRegexNoMatch(LDAPSyntaxValueError):
    """
    Exception raised in case a regex pattern check failed
    """


class LDAPSyntax:
    """
    Base class for all LDAP syntax and attribute value plugin classes
    """
    __slots__ = (
        '_app',
        '_at',
        '_av',
        '_av_u',
        '_dn',
        '_entry',
        '_schema',
    )
    oid: str = ''
    desc: str = 'Any LDAP syntax'
    input_size: int = 50
    max_len: int = web2ldapcnf.input_maxfieldlen
    max_values: int = web2ldapcnf.input_maxattrs
    mime_type: str = 'application/octet-stream'
    file_ext: str = 'bin'
    editable: bool = True
    pattern: Optional[Pattern[str]] = None
    input_pattern: Optional[str] = None
    search_sep: str = '<br>'
    read_sep: str = '<br>'
    field_sep: str = '<br>'
    sani_funcs: Sequence[Callable] = (())
    show_val_button: bool = True

    def __init__(
            self,
            app,
            dn: Optional[str],
            schema: SubSchema,
            attrType: Optional[str],
            attr_value: Optional[bytes],
            entry=None,
        ):
        if not entry:
            entry = ldap0.schema.models.Entry(schema, dn, {})
        assert isinstance(dn, str), \
            TypeError("Argument 'dn' must be str, was %r" % (dn,))
        assert isinstance(attrType, str) or attrType is None, \
            TypeError("Argument 'attrType' must be str or None, was %r" % (attrType,))
        assert isinstance(attr_value, bytes) or attr_value is None, \
            TypeError("Argument 'attr_value' must be bytes or None, was %r" % (attr_value,))
        assert entry is None or isinstance(entry, ldap0.schema.models.Entry), \
            TypeError('entry must be ldaputil.schema.Entry, was %r' % (entry,))
        self._at = attrType
        self._av = attr_value
        self._av_u = None
        self._app = app
        self._schema = schema
        self._dn = dn
        self._entry = entry

    @property
    def dn(self):
        return DNObj.from_str(self._dn)

    @property
    def av_u(self):
        if (self._av is not None and self._av_u is None):
            self._av_u = self._av.decode(self._app.ls.charset)
        return self._av_u

    def sanitize(self, attr_value: bytes) -> bytes:
        """
        Transforms the HTML form input field values into LDAP string
        representations and returns raw binary string.

        This is the inverse of LDAPSyntax.form_value().

        When using this method one MUST NOT assume that the whole entry is
        present.
        """
        for sani_func in self.sani_funcs:
            attr_value = sani_func(attr_value)
        return attr_value

    def transmute(self, attr_values: List[bytes]) -> List[bytes]:
        """
        This method can be implemented to transmute attribute values and has
        to handle LDAP string representations (raw binary strings).

        This method has access to the whole entry after processing all input.

        Implementors should be prepared that this method could be called
        more than once. If there's nothing to change then simply return the
        same value list.

        Exceptions KeyError or IndexError are caught by the calling code to
        re-iterate invoking this method.
        """
        return attr_values

    def _validate(self, attr_value: bytes) -> bool:
        """
        check the syntax of attr_value

        Implementors can overload this method to apply arbitrary syntax checks.
        """
        return True

    def validate(self, attr_value: bytes):
        if not attr_value:
            return
        if self.pattern and (self.pattern.match(attr_value.decode(self._app.ls.charset)) is None):
            raise LDAPSyntaxRegexNoMatch(
                "Class %s: %r does not match pattern %r." % (
                    self.__class__.__name__,
                    attr_value,
                    self.pattern.pattern,
                )
            )
        if not self._validate(attr_value):
            raise LDAPSyntaxValueError(
                "Class %s: %r does not comply to syntax (attr type %r)." % (
                    self.__class__.__name__,
                    attr_value,
                    self._at,
                )
            )
        # end of validate()

    def value_button(self, command, row, mode, link_text=None) -> str:
        """
        return HTML markup of [+] or [-] submit buttons for adding/removing
        attribute values

        row
          row number in input table
        mode
          '+' or '-'
        link_text
          optionally override displayed link link_text
        """
        link_text = link_text or mode
        if (
                not self.show_val_button or
                self.max_values <= 1 or
                len(self._entry.get(self._at, [])) >= self.max_values
            ):
            return ''
        se_obj = self._schema.get_obj(AttributeType, self._at)
        if se_obj and se_obj.single_value:
            return ''
        return (
            '<button'
            ' formaction="%s#in_a_%s"'
            ' type="submit"'
            ' name="in_mr"'
            ' value="%s%d">%s'
            '</button>'
        ) % (
            self._app.form.action_url(command, self._app.sid),
            self._app.form.s2d(self._at),
            mode, row, link_text
        )

    def form_value(self) -> str:
        """
        Transform LDAP string representations to HTML form input field
        values. Returns Unicode string to be encoded with the browser's
        accepted charset.

        This is the inverse of LDAPSyntax.sanitize().
        """
        try:
            result = self.av_u or ''
        except UnicodeDecodeError:
            result = '!!!snipped because of UnicodeDecodeError!!!'
        return result

    def input_fields(self):
        return (self.input_field(),)

    def input_field(self) -> web_forms.Field:
        input_field = web_forms.Input(
            self._at,
            ': '.join([self._at, self.desc]),
            self.max_len,
            self.max_values,
            self.input_pattern,
            default=None,
            size=min(self.max_len, self.input_size),
        )
        input_field.charset = self._app.form.accept_charset
        input_field.set_default(self.form_value())
        return input_field

    def display(self, vidx, links) -> str:
        try:
            res = self._app.form.s2d(self.av_u)
        except UnicodeDecodeError:
            res = self._app.form.s2d(repr(self._av))
        return res


class Binary(LDAPSyntax):
    """
    Plugin class for LDAP syntax 'Binary' (see RFC 2252)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.5'
    desc: str = 'Binary'
    editable: bool = False

    def input_field(self) -> web_forms.Field:
        field = web_forms.File(
            self._at,
            ': '.join([self._at, self.desc]),
            self.max_len, self.max_values, None, default=self._av, size=50
        )
        field.mime_type = self.mime_type
        return field

    def display(self, vidx, links) -> str:
        return '%d bytes | %s' % (
            len(self._av),
            self._app.anchor(
                'read', 'View/Load',
                [
                    ('dn', self._dn),
                    ('read_attr', self._at),
                    ('read_attrindex', str(vidx)),
                ],
            )
        )


class Audio(Binary):
    """
    Plugin class for LDAP syntax 'Audio' (see RFC 2252)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.4'
    desc: str = 'Audio'
    mime_type: str = 'audio/basic'
    file_ext: str = 'au'

    def _validate(self, attr_value: bytes) -> bool:
        with BytesIO(attr_value) as fileobj:
            res = sndhdr.test_au(attr_value, fileobj)
        return res is not None

    def display(self, vidx, links) -> str:
        mimetype = self.mime_type
        return (
            '<embed type="%s" autostart="false" '
            'src="%s?dn=%s&amp;read_attr=%s&amp;read_attrindex=%d">'
            '%d bytes of audio data (%s)'
        ) % (
            mimetype,
            self._app.form.action_url('read', self._app.sid),
            urllib.parse.quote(self._dn.encode(self._app.form.accept_charset)),
            urllib.parse.quote(self._at),
            vidx,
            len(self._av),
            mimetype
        )


class DirectoryString(LDAPSyntax):
    """
    Plugin class for LDAP syntax 'Directory String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.6)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.15'
    desc: str = 'Directory String'
    html_tmpl = '{av}'

    def _validate(self, attr_value: bytes) -> bool:
        try:
            attr_value.decode(self._app.ls.charset)
        except UnicodeDecodeError:
            return False
        return True

    def display(self, vidx, links) -> str:
        return self.html_tmpl.format(
            av=self._app.form.s2d(self.av_u)
        )


class DistinguishedName(DirectoryString):
    """
    Plugin class for LDAP syntax 'DN'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.9)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.12'
    desc: str = 'Distinguished Name'
    isBindDN = False
    hasSubordinates = False
    ref_attrs: Optional[Sequence[Tuple[Optional[str], str, Optional[str], str]]] = None

    def _validate(self, attr_value: bytes) -> bool:
        return is_dn(attr_value.decode(self._app.ls.charset))

    def _additional_links(self):
        res = []
        if self._at.lower() != 'entrydn':
            res.append(
                self._app.anchor(
                    'read', 'Read',
                    [('dn', self.av_u)],
                )
            )
        if self.hasSubordinates:
            res.append(self._app.anchor(
                'search', 'Down',
                (
                    ('dn', self.av_u),
                    ('scope', SEARCH_SCOPE_STR_ONELEVEL),
                    ('filterstr', '(objectClass=*)'),
                )
            ))
        if self.isBindDN:
            ldap_url_obj = self._app.ls.ldap_url('', add_login=False)
            res.append(
                self._app.anchor(
                    'login',
                    'Bind as',
                    [
                        ('ldapurl', str(ldap_url_obj)),
                        ('dn', self._dn),
                        ('login_who', self.av_u),
                    ],
                    title='Connect and bind new session as\r\n%s' % (self.av_u)
                ),
            )
        # If self.ref_attrs is not empty then add links for searching back-linking entries
        for ref_attr_tuple in self.ref_attrs or tuple():
            try:
                ref_attr, ref_text, ref_dn, ref_oc, ref_title = ref_attr_tuple
            except ValueError:
                ref_oc = None
                ref_attr, ref_text, ref_dn, ref_title = ref_attr_tuple
            ref_attr = ref_attr or self._at
            if ref_attr not in self._schema.name2oid[AttributeType]:
                continue
            ref_dn = ref_dn or self._dn
            ref_title = ref_title or 'Search %s entries referencing entry %s in attribute %s' % (
                ref_oc, self.av_u, ref_attr,
            )
            res.append(self._app.anchor(
                'search', self._app.form.s2d(ref_text),
                (
                    ('dn', ref_dn),
                    ('search_root', str(self._app.naming_context)),
                    ('searchform_mode', 'adv'),
                    ('search_attr', 'objectClass'),
                    (
                        'search_option',
                        {
                            True: SEARCH_OPT_ATTR_EXISTS,
                            False: SEARCH_OPT_IS_EQUAL,
                        }[ref_oc is None]
                    ),
                    ('search_string', ref_oc or ''),
                    ('search_attr', ref_attr),
                    ('search_option', SEARCH_OPT_IS_EQUAL),
                    ('search_string', self.av_u),
                ),
                title=ref_title,
            ))
        return res

    def display(self, vidx, links) -> str:
        res = [self._app.form.s2d(self.av_u or '- World -')]
        if links:
            res.extend(self._additional_links())
        return web2ldapcnf.command_link_separator.join(res)


class BindDN(DistinguishedName):
    """
    Plugin class for DNs probably usable as bind-DN
    """
    oid: str = 'BindDN-oid'
    desc: str = 'A Distinguished Name used to bind to a directory'
    isBindDN = True


class AuthzDN(DistinguishedName):
    """
    Plugin class for DNs used for authorization
    """
    oid: str = 'AuthzDN-oid'
    desc: str = 'Authz Distinguished Name'

    def display(self, vidx, links) -> str:
        result = DistinguishedName.display(self, vidx, links)
        if links:
            simple_display_str = DistinguishedName.display(
                self,
                vidx,
                links=False,
            )
            whoami_display_str = self._app.display_authz_dn(who=self.av_u)
            if whoami_display_str != simple_display_str:
                result = '<br>'.join((whoami_display_str, result))
        return result


class NameAndOptionalUID(DistinguishedName):
    """
    Plugin class for LDAP syntax 'Name and Optional UID'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.21)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.34'
    desc: str = 'Name And Optional UID'

    @staticmethod
    def _split_dn_and_uid(val: str) -> Tuple[str, Optional[str]]:
        try:
            sep_ind = val.rindex('#')
        except ValueError:
            dn = val
            uid = None
        else:
            dn = val[0:sep_ind]
            uid = val[sep_ind+1:]
        return dn, uid

    def _validate(self, attr_value: bytes) -> bool:
        dn, _ = self._split_dn_and_uid(attr_value.decode(self._app.ls.charset))
        return is_dn(dn)

    def display(self, vidx, links) -> str:
        value = self.av_u.split('#')
        dn_str = self._app.display_dn(
            self.av_u,
            links=links,
        )
        if len(value) == 1 or not value[1]:
            return dn_str
        return web2ldapcnf.command_link_separator.join([
            self._app.form.s2d(value[1]),
            dn_str,
        ])


class BitString(DirectoryString):
    """
    Plugin class for LDAP syntax 'Bit String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.2)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.6'
    desc: str = 'Bit String'
    pattern = re.compile("^'[01]+'B$")


class IA5String(DirectoryString):
    """
    Plugin class for LDAP syntax 'IA5 String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.15)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.26'
    desc: str = 'IA5 String'

    def _validate(self, attr_value: bytes) -> bool:
        try:
            _ = attr_value.decode('ascii').encode('ascii')
        except UnicodeError:
            return False
        return True


class GeneralizedTime(IA5String):
    """
    Plugin class for LDAP syntax 'Generalized Time'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.13)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.24'
    desc: str = 'Generalized Time'
    input_size: int = 24
    max_len: int = 24
    pattern = re.compile(r'^([0-9]){12,14}((\.|,)[0-9]+)*(Z|(\+|-)[0-9]{4})$')
    timeDefault = None
    notBefore = None
    notAfter = None
    form_value_fmt = '%Y-%m-%dT%H:%M:%SZ'
    dtFormats = (
        '%Y%m%d%H%M%SZ',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%MZ',
        '%Y-%m-%dT%H:%M:%S+00:00',
        '%Y-%m-%dT%H:%M:%S-00:00',
        '%Y-%m-%d %H:%M:%SZ',
        '%Y-%m-%d %H:%MZ',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S+00:00',
        '%Y-%m-%d %H:%M:%S-00:00',
        '%d.%m.%YT%H:%M:%SZ',
        '%d.%m.%YT%H:%MZ',
        '%d.%m.%YT%H:%M:%S+00:00',
        '%d.%m.%YT%H:%M:%S-00:00',
        '%d.%m.%Y %H:%M:%SZ',
        '%d.%m.%Y %H:%MZ',
        '%d.%m.%Y %H:%M',
        '%d.%m.%Y %H:%M:%S+00:00',
        '%d.%m.%Y %H:%M:%S-00:00',
    )
    acceptable_formats = (
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%m/%d/%Y',
    )
    dt_display_format = (
        '<time datetime="%Y-%m-%dT%H:%M:%SZ">'
        '%A (%W. week) %Y-%m-%d %H:%M:%S+00:00'
        '</time>'
    )

    def _validate(self, attr_value: bytes) -> bool:
        try:
            d_t = utc_strptime(attr_value)
        except ValueError:
            return False
        return (
            (self.notBefore is None or self.notBefore <= d_t)
            and (self.notAfter is None or self.notAfter >= d_t)
        )

    def form_value(self) -> str:
        if not self._av:
            return ''
        try:
            d_t = datetime.datetime.strptime(self.av_u, r'%Y%m%d%H%M%SZ')
        except ValueError:
            result = IA5String.form_value(self)
        else:
            result = str(datetime.datetime.strftime(d_t, self.form_value_fmt))
        return result

    def sanitize(self, attr_value: bytes) -> bytes:
        av_u = attr_value.strip().upper().decode(self._app.ls.charset)
        # Special cases first
        if av_u in {'N', 'NOW', '0'}:
            return datetime.datetime.strftime(
                datetime.datetime.utcnow(),
                r'%Y%m%d%H%M%SZ',
            ).encode('ascii')
        # a single integer value is interpreted as seconds relative to now
        try:
            float_val = float(av_u)
        except ValueError:
            pass
        else:
            return datetime.datetime.strftime(
                datetime.datetime.utcnow()+datetime.timedelta(seconds=float_val),
                r'%Y%m%d%H%M%SZ',
            ).encode('ascii')
        if self.timeDefault:
            date_format = r'%Y%m%d' + self.timeDefault + 'Z'
            if av_u in ('T', 'TODAY'):
                return datetime.datetime.strftime(
                    datetime.datetime.utcnow(),
                    date_format,
                ).encode('ascii')
            if av_u in ('Y', 'YESTERDAY'):
                return datetime.datetime.strftime(
                    datetime.datetime.today()-datetime.timedelta(days=1),
                    date_format,
                ).encode('ascii')
            if av_u in ('T', 'TOMORROW'):
                return datetime.datetime.strftime(
                    datetime.datetime.today()+datetime.timedelta(days=1),
                    date_format,
                ).encode('ascii')
        # Try to parse various datetime syntaxes
        for time_format in self.dtFormats:
            try:
                d_t = datetime.datetime.strptime(av_u, time_format)
            except ValueError:
                result = None
            else:
                result = datetime.datetime.strftime(d_t, r'%Y%m%d%H%M%SZ')
                break
        if result is None:
            if self.timeDefault:
                for time_format in self.acceptable_formats or []:
                    try:
                        d_t = datetime.datetime.strptime(av_u, time_format)
                    except ValueError:
                        result = None
                    else:
                        result = datetime.datetime.strftime(d_t, r'%Y%m%d'+self.timeDefault+'Z')
                        break
            else:
                result = av_u
        if result is None:
            return IA5String.sanitize(self, attr_value)
        return result.encode('ascii')
        # end of GeneralizedTime.sanitize()

    def display(self, vidx, links) -> str:
        try:
            dt_utc = utc_strptime(self.av_u)
        except ValueError:
            return IA5String.display(self, vidx, links)
        try:
            dt_utc_str = dt_utc.strftime(self.dt_display_format)
        except ValueError:
            return IA5String.display(self, vidx, links)
        if not links:
            return dt_utc_str
        current_time = datetime.datetime.utcnow()
        time_span = (current_time - dt_utc).total_seconds()
        return '{dt_utc} ({av})<br>{timespan_disp} {timespan_comment}'.format(
            dt_utc=dt_utc_str,
            av=self._app.form.s2d(self.av_u),
            timespan_disp=self._app.form.s2d(
                ts2repr(Timespan.time_divisors, ' ', abs(time_span))
            ),
            timespan_comment={
                1: 'ago',
                0: '',
                -1: 'ahead',
            }[cmp(time_span, 0)]
        )


class NotBefore(GeneralizedTime):
    """
    Plugin class for attributes indicating start of a period
    """
    oid: str = 'NotBefore-oid'
    desc: str = 'A not-before timestamp by default starting at 00:00:00'
    timeDefault = '000000'


class NotAfter(GeneralizedTime):
    """
    Plugin class for attributes indicating end of a period
    """
    oid: str = 'NotAfter-oid'
    desc: str = 'A not-after timestamp by default ending at 23:59:59'
    timeDefault = '235959'


class UTCTime(GeneralizedTime):
    """
    Plugin class for LDAP syntax 'UTC Time'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.34)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.53'
    desc: str = 'UTC Time'


class NullTerminatedDirectoryString(DirectoryString):
    """
    Plugin class for strings terminated with null-byte
    """
    oid: str = 'NullTerminatedDirectoryString-oid'
    desc: str = 'Directory String terminated by null-byte'

    def sanitize(self, attr_value: bytes) -> bytes:
        return attr_value + b'\x00'

    def _validate(self, attr_value: bytes) -> bool:
        return attr_value.endswith(b'\x00')

    def form_value(self) -> str:
        return (self._av or b'\x00')[:-1].decode(self._app.ls.charset)

    def display(self, vidx, links) -> str:
        return self._app.form.s2d(
            (self._av or b'\x00')[:-1].decode(self._app.ls.charset)
        )


class OtherMailbox(DirectoryString):
    """
    Plugin class for LDAP syntax 'Other Mailbox'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.27)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.39'
    desc: str = 'Other Mailbox'
    charset = 'ascii'


class Integer(IA5String):
    """
    Plugin class for LDAP syntax 'Integer'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.16)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.27'
    desc: str = 'Integer'
    input_size: int = 12
    min_value = None
    max_value = None

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attr_value, entry)
        if self.max_value is not None:
            self.max_len = len(str(self.max_value))

    def _maxlen(self, fval: str) -> int:
        min_value_len = max_value_len = fval_len = 0
        if self.min_value is not None:
            min_value_len = len(str(self.min_value))
        if self.max_value is not None:
            max_value_len = len(str(self.max_value))
        if fval is not None:
            fval_len = len(fval.encode(self._app.ls.charset))
        return max(self.input_size, fval_len, min_value_len, max_value_len)

    def _validate(self, attr_value: bytes) -> bool:
        try:
            val = int(attr_value)
        except ValueError:
            return False
        min_value, max_value = self.min_value, self.max_value
        return (
            (min_value is None or val >= min_value) and
            (max_value is None or val <= max_value)
        )

    def sanitize(self, attr_value: bytes) -> bytes:
        try:
            return str(int(attr_value)).encode('ascii')
        except ValueError:
            return attr_value

    def input_field(self) -> web_forms.Field:
        fval = self.form_value()
        max_len = self._maxlen(fval)
        input_field = web_forms.Input(
            self._at,
            ': '.join([self._at, self.desc]),
            max_len,
            self.max_values,
            self.input_pattern,
            default=fval,
            size=min(self.input_size, max_len),
        )
        input_field.input_type = 'number'
        return input_field


class IPHostAddress(IA5String):
    """
    Plugin class for string representation of IPv4 or IPv6 host address
    """
    oid: str = 'IPHostAddress-oid'
    desc: str = 'string representation of IPv4 or IPv6 address'
    # Class in module ipaddr which parses address/network values
    addr_class = None
    sani_funcs = (
        bytes.strip,
    )

    def _validate(self, attr_value: bytes) -> bool:
        try:
            addr = ipaddress.ip_address(attr_value.decode('ascii'))
        except ValueError:
            return False
        return self.addr_class is None or isinstance(addr, self.addr_class)


class IPv4HostAddress(IPHostAddress):
    """
    Plugin class for string representation of IPv4 host address
    """
    oid: str = 'IPv4HostAddress-oid'
    desc: str = 'string representation of IPv4 address'
    addr_class = ipaddress.IPv4Address


class IPv6HostAddress(IPHostAddress):
    """
    Plugin class for string representation of IPv6 host address
    """
    oid: str = 'IPv6HostAddress-oid'
    desc: str = 'string representation of IPv6 address'
    addr_class = ipaddress.IPv6Address


class IPNetworkAddress(IPHostAddress):
    """
    Plugin class for string representation of IPv4 or IPv6 network address
    """
    oid: str = 'IPNetworkAddress-oid'
    desc: str = 'string representation of IPv4 or IPv6 network address/mask'

    def _validate(self, attr_value: bytes) -> bool:
        try:
            addr = ipaddress.ip_network(attr_value.decode('ascii'), strict=False)
        except ValueError:
            return False
        return self.addr_class is None or isinstance(addr, self.addr_class)


class IPv4NetworkAddress(IPNetworkAddress):
    """
    Plugin class for string representation of IPv4 network address
    """
    oid: str = 'IPv4NetworkAddress-oid'
    desc: str = 'string representation of IPv4 network address/mask'
    addr_class = ipaddress.IPv4Network


class IPv6NetworkAddress(IPNetworkAddress):
    """
    Plugin class for string representation of IPv6 network address
    """
    oid: str = 'IPv6NetworkAddress-oid'
    desc: str = 'string representation of IPv6 network address/mask'
    addr_class = ipaddress.IPv6Network


class IPServicePortNumber(Integer):
    """
    Plugin class for service port number (see /etc/services)
    """
    oid: str = 'IPServicePortNumber-oid'
    desc: str = 'Port number for an UDP- or TCP-based service'
    min_value = 0
    max_value = 65535


class MacAddress(IA5String):
    """
    Plugin class for IEEEE MAC addresses of network devices
    """
    oid: str = 'MacAddress-oid'
    desc: str = 'MAC address in hex-colon notation'
    min_len: int = 17
    max_len: int = 17
    pattern = re.compile(r'^([0-9a-f]{2}\:){5}[0-9a-f]{2}$')

    def sanitize(self, attr_value: bytes) -> bytes:
        attr_value = attr_value.translate(None, b'.-: ').lower().strip()
        if len(attr_value) == 12:
            return b':'.join([attr_value[i*2:i*2+2] for i in range(6)])
        return attr_value


class Uri(DirectoryString):
    """
    Plugin class for Uniform Resource Identifiers (URIs, see RFC 2079)
    """
    oid: str = 'Uri-OID'
    desc: str = 'URI'
    pattern = re.compile(r'^(ftp|http|https|news|snews|ldap|ldaps|mailto):(|//)[^ ]*')
    sani_funcs = (
        bytes.strip,
    )

    def display(self, vidx, links) -> str:
        attr_value = self.av_u
        try:
            url, label = attr_value.split(' ', 1)
        except ValueError:
            url, label = attr_value, attr_value
            display_url = ''
        else:
            display_url = ' (%s)' % (url)
        if ldap0.ldapurl.is_ldapurl(url):
            return '<a href="%s?%s">%s%s</a>' % (
                self._app.form.script_name,
                self._app.form.s2d(url),
                self._app.form.s2d(label),
                self._app.form.s2d(display_url),
            )
        if url.lower().find('javascript:') >= 0:
            return '<code>%s</code>' % (
                DirectoryString.display(self, vidx=False, links=False)
            )
        return '<a href="%s?%s">%s%s</a>' % (
            self._app.form.action_url('urlredirect', self._app.sid),
            self._app.form.s2d(url),
            self._app.form.s2d(label),
            self._app.form.s2d(display_url),
        )


class Image(Binary):
    """
    Plugin base class for attributes containing image data.
    """
    oid: str = 'Image-OID'
    desc: str = 'Image base class'
    mime_type: str = 'application/octet-stream'
    file_ext: str = 'bin'
    imageFormat = None
    inline_maxlen = 630  # max. number of bytes to use data: URI instead of external URL

    def _validate(self, attr_value: bytes) -> bool:
        return imghdr.what(None, attr_value) == self.imageFormat.lower()

    def sanitize(self, attr_value: bytes) -> bytes:
        if not self._validate(attr_value) and PIL_AVAIL:
            try:
                with BytesIO(attr_value) as imgfile:
                    img = PILImage.open(imgfile)
                    imgfile.seek(0)
                    img.save(imgfile, self.imageFormat)
                    attr_value = imgfile.getvalue()
            except Exception as err:
                logger.warning(
                    'Error converting image data (%d bytes) to %s: %r',
                    len(attr_value),
                    self.imageFormat,
                    err,
                )
        return attr_value

    def display(self, vidx, links) -> str:
        maxwidth, maxheight = 100, 150
        width, height = None, None
        size_attr_html = ''
        if PIL_AVAIL:
            try:
                with BytesIO(self._av) as imgfile:
                    img = PILImage.open(imgfile)
            except IOError:
                pass
            else:
                width, height = img.size
                if width > maxwidth:
                    size_attr_html = 'width="%d" height="%d"' % (
                        maxwidth,
                        int(float(maxwidth)/width*height),
                    )
                elif height > maxheight:
                    size_attr_html = 'width="%d" height="%d"' % (
                        int(float(maxheight)/height*width),
                        maxheight,
                    )
                else:
                    size_attr_html = 'width="%d" height="%d"' % (width, height)
        attr_value_len = len(self._av)
        img_link = '%s?dn=%s&amp;read_attr=%s&amp;read_attrindex=%d' % (
            self._app.form.action_url('read', self._app.sid),
            urllib.parse.quote(self._dn),
            urllib.parse.quote(self._at),
            vidx,
        )
        if attr_value_len <= self.inline_maxlen:
            return (
                '<a href="%s">'
                '<img src="data:%s;base64,\n%s" alt="%d bytes of image data" %s>'
                '</a>'
            ) % (
                img_link,
                self.mime_type,
                self._av.encode('base64'),
                attr_value_len,
                size_attr_html,
            )
        return '<a href="%s"><img src="%s" alt="%d bytes of image data" %s></a>' % (
            img_link,
            img_link,
            attr_value_len,
            size_attr_html,
        )


class JPEGImage(Image):
    """
    Plugin class for LDAP syntax 'JPEG'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.17)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.28'
    desc: str = 'JPEG image'
    mime_type: str = 'image/jpeg'
    file_ext: str = 'jpg'
    imageFormat = 'JPEG'


class PhotoG3Fax(Binary):
    """
    Plugin class for LDAP syntax 'Fax'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.12)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.23'
    desc: str = 'Photo (G3 fax)'
    mime_type: str = 'image/g3fax'
    file_ext: str = 'tif'


class OID(IA5String):
    """
    Plugin class for LDAP syntax 'OID'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.26)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.38'
    desc: str = 'OID'
    pattern = re.compile(r'^([a-zA-Z]+[a-zA-Z0-9;-]*|[0-2]?\.([0-9]+\.)*[0-9]+)$')
    no_val_button_attrs = frozenset((
        'objectclass',
        'structuralobjectclass',
        '2.5.4.0',
        '2.5.21.9',
    ))

    def value_button(self, command, row, mode, link_text=None) -> str:
        if self._at.lower() in self.no_val_button_attrs:
            return ''
        return IA5String.value_button(self, command, row, mode, link_text=link_text)

    def sanitize(self, attr_value: bytes) -> bytes:
        return attr_value.strip()

    def display(self, vidx, links) -> str:
        try:
            name, description, reference = OID_REG[self.av_u]
        except (KeyError, ValueError):
            try:
                se_obj = self._schema.get_obj(
                    ObjectClass,
                    self.av_u,
                    raise_keyerror=1,
                )
            except KeyError:
                try:
                    se_obj = self._schema.get_obj(
                        AttributeType,
                        self.av_u,
                        raise_keyerror=1,
                    )
                except KeyError:
                    return IA5String.display(self, vidx, links)
                return schema_anchor(
                    self._app,
                    self.av_u,
                    AttributeType,
                    name_template='{name}\n{anchor}',
                    link_text='&raquo;',
                )
            if self._at.lower() == 'structuralobjectclass':
                name_template = '{name}\n{anchor}'
            else:
                name_template = '{name}\n (%s){anchor}' % (OBJECTCLASS_KIND_STR[se_obj.kind],)
            # objectClass attribute is displayed with different function
            return schema_anchor(
                self._app,
                self.av_u,
                ObjectClass,
                name_template=name_template,
                link_text='&raquo;',
            )
        return '<strong>%s</strong> (%s):<br>%s (see %s)' % (
            self._app.form.s2d(name),
            IA5String.display(self, vidx, links),
            self._app.form.s2d(description),
            self._app.form.s2d(reference)
        )


class LDAPUrl(Uri):
    """
    Plugin class for attributes containing LDAP URLs
    """
    oid: str = 'LDAPUrl-oid'
    desc: str = 'LDAP URL'

    def _command_ldap_url(self, ldap_url: str) -> Union[str, ldap0.ldapurl.LDAPUrl]:
        return ldap_url

    def display(self, vidx, links) -> str:
        try:
            if links:
                linksstr = self._app.ldap_url_anchor(
                    self._command_ldap_url(self.av_u),
                )
            else:
                linksstr = ''
        except ValueError:
            return '<strong>Not a valid LDAP URL:</strong> %s' % (
                self._app.form.s2d(repr(self._av))
            )
        return '<table><tr><td>%s</td><td><a href="%s">%s</a></td></tr></table>' % (
            linksstr,
            self._app.form.s2d(self.av_u),
            self._app.form.s2d(self.av_u)
        )


class OctetString(Binary):
    """
    Plugin class for LDAP syntax 'Octet String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.25)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.40'
    desc: str = 'Octet String'
    editable: bool = True
    min_input_rows = 1  # minimum number of rows for input field
    max_input_rows = 15 # maximum number of rows for in input field
    bytes_split = 16

    def sanitize(self, attr_value: bytes) -> bytes:
        attr_value = attr_value.translate(None, b': ,\r\n')
        try:
            res = binascii.unhexlify(attr_value)
        except binascii.Error:
            res = attr_value
        return res

    def display(self, vidx, links) -> str:
        lines = [
            (
                '<tr>'
                '<td><code>%0.6X</code></td>'
                '<td><code>%s</code></td>'
                '<td><code>%s</code></td>'
                '</tr>'
            ) % (
                i*self.bytes_split,
                ':'.join(c[j:j+1].hex().upper() for j in range(len(c))),
                self._app.form.s2d(ascii_dump(c), 'ascii'),
            )
            for i, c in enumerate(chunks(self._av, self.bytes_split))
        ]
        return '\n<table class="HexDump">\n%s\n</table>\n' % ('\n'.join(lines))

    def form_value(self) -> str:
        hex_av = (self._av or b'').hex().upper()
        hex_range = range(0, len(hex_av), 2)
        return str('\r\n'.join(
            chunks(
                ':'.join([hex_av[i:i+2] for i in hex_range]),
                self.bytes_split*3
            )
        ))

    def input_field(self) -> web_forms.Field:
        fval = self.form_value()
        return web_forms.Textarea(
            self._at,
            ': '.join([self._at, self.desc]),
            10000, 1,
            None,
            default=fval,
            rows=max(self.min_input_rows, min(self.max_input_rows, fval.count('\r\n'))),
            cols=49
        )


class MultilineText(DirectoryString):
    """
    Plugin base class for multi-line text.
    """
    oid: str = 'MultilineText-oid'
    desc: str = 'Multiple lines of text'
    pattern = re.compile('^.*$', re.S+re.M)
    lineSep = b'\r\n'
    mime_type: str = 'text/plain'
    cols = 66
    min_input_rows = 1   # minimum number of rows for input field
    max_input_rows = 30  # maximum number of rows for in input field

    def _split_lines(self, value):
        if self.lineSep:
            return value.split(self.lineSep)
        return [value]

    def sanitize(self, attr_value: bytes) -> bytes:
        return attr_value.replace(
            b'\r', b''
        ).replace(
            b'\n', self.lineSep
        )

    def display(self, vidx, links) -> str:
        return '<br>'.join([
            self._app.form.s2d(line_b.decode(self._app.ls.charset))
            for line_b in self._split_lines(self._av)
        ])

    def form_value(self) -> str:
        splitted_lines = [
            line_b.decode(self._app.ls.charset)
            for line_b in self._split_lines(self._av or b'')
        ]
        return '\r\n'.join(splitted_lines)

    def input_field(self) -> web_forms.Field:
        fval = self.form_value()
        return web_forms.Textarea(
            self._at,
            ': '.join([self._at, self.desc]),
            self.max_len, self.max_values,
            None,
            default=fval,
            rows=max(self.min_input_rows, min(self.max_input_rows, fval.count('\r\n'))),
            cols=self.cols
        )


class PreformattedMultilineText(MultilineText):
    """
    Plugin base class for multi-line text displayed with mono-spaced font,
    e.g. program code, XML, JSON etc.
    """
    oid: str = 'PreformattedMultilineText-oid'
    cols = 66
    tab_identiation = '&nbsp;&nbsp;&nbsp;&nbsp;'

    def display(self, vidx, links) -> str:
        lines = [
            self._app.form.s2d(
                line_b.decode(self._app.ls.charset),
                self.tab_identiation,
            )
            for line_b in self._split_lines(self._av)
        ]
        return '<code>%s</code>' % '<br>'.join(lines)


class PostalAddress(MultilineText):
    """
    Plugin class for LDAP syntax 'Postal Address'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.28)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.41'
    desc: str = 'Postal Address'
    lineSep = b' $ '
    cols = 40

    def _split_lines(self, value):
        return [
            v.strip()
            for v in value.split(self.lineSep.strip())
        ]

    def sanitize(self, attr_value: bytes) -> bytes:
        return attr_value.replace(b'\r', b'').replace(b'\n', self.lineSep)


class PrintableString(DirectoryString):
    """
    Plugin class for LDAP syntax 'Printable String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.29)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.44'
    desc: str = 'Printable String'
    pattern = re.compile("^[a-zA-Z0-9'()+,.=/:? -]*$")
    charset = 'ascii'


class NumericString(PrintableString):
    """
    Plugin class for LDAP syntax 'Numeric String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.23)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.36'
    desc: str = 'Numeric String'
    pattern = re.compile('^[ 0-9]+$')


class EnhancedGuide(PrintableString):
    """
    Plugin class for LDAP syntax 'Enhanced Guide'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.10)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.21'
    desc: str = 'Enhanced Search Guide'


class Guide(EnhancedGuide):
    """
    Plugin class for LDAP syntax 'Search Guide'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.14)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.25'
    desc: str = 'Search Guide'


class TelephoneNumber(PrintableString):
    """
    Plugin class for LDAP syntax ''
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.31)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.50'
    desc: str = 'Telephone Number'
    pattern = re.compile('^[0-9+x(). /-]+$')

    def sanitize(self, attr_value: bytes) -> bytes:
        if PHONENUMBERS_AVAIL:
            try:
                attr_value = phonenumbers.format_number(
                    phonenumbers.parse(
                        attr_value.decode('ascii'),
                        region=(
                            self._entry['c'][0].decode('ascii')
                            if 'c' in self._entry
                            else None
                        ),
                    ),
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL,
                ).encode('ascii')
            except (
                    UnicodeDecodeError,
                    ValueError,
                    phonenumbers.phonenumberutil.NumberParseException,
                ):
                attr_value = PrintableString.sanitize(self, attr_value)
        else:
            attr_value = PrintableString.sanitize(self, attr_value)
        return attr_value


class FacsimileTelephoneNumber(TelephoneNumber):
    """
    Plugin class for LDAP syntax 'Facsimile Telephone Number'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.11)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.22'
    desc: str = 'Facsimile Number'
    pattern = re.compile(
        r'^[0-9+x(). /-]+'
        r'(\$'
        r'(twoDimensional|fineResolution|unlimitedLength|b4Length|a3Width|b4Width|uncompressed)'
        r')*$'
    )


class TelexNumber(PrintableString):
    """
    Plugin class for LDAP syntax 'Telex Number'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.33)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.52'
    desc: str = 'Telex Number'
    pattern = re.compile("^[a-zA-Z0-9'()+,.=/:?$ -]*$")


class TeletexTerminalIdentifier(PrintableString):
    """
    Plugin class for LDAP syntax 'Teletex Terminal Identifier'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.32)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.51'
    desc: str = 'Teletex Terminal Identifier'


class ObjectGUID(LDAPSyntax):
    oid: str = 'ObjectGUID-oid'
    desc: str = 'Object GUID'
    charset = 'ascii'

    def display(self, vidx, links) -> str:
        objectguid_str = ''.join([
            '%02X' % ord(c)
            for c in self._av
        ])
        return ldap0.ldapurl.LDAPUrl(
            ldapUrl=self._app.ls.uri,
            dn='GUID=%s' % (objectguid_str),
            who=None, cred=None
        ).htmlHREF(
            hrefText=objectguid_str,
            hrefTarget=None
        )


class Date(IA5String):
    """
    Plugin base class for a date without(!) time component.
    """
    oid: str = 'Date-oid'
    desc: str = 'Date in syntax specified by class attribute storage_format'
    max_len: int = 10
    storage_format = '%Y-%m-%d'
    acceptable_formats = (
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%m/%d/%Y',
    )

    def _validate(self, attr_value: bytes) -> bool:
        try:
            datetime.datetime.strptime(
                attr_value.decode(self._app.ls.charset),
                self.storage_format
            )
        except (UnicodeDecodeError, ValueError):
            return False
        return True

    def sanitize(self, attr_value: bytes) -> bytes:
        av_u = attr_value.strip().decode(self._app.ls.charset)
        result = attr_value
        for time_format in self.acceptable_formats:
            try:
                time_tuple = datetime.datetime.strptime(av_u, time_format)
            except ValueError:
                pass
            else:
                result = datetime.datetime.strftime(time_tuple, self.storage_format).encode('ascii')
                break
        return result # sanitize()


class NumstringDate(Date):
    """
    Plugin class for a date using syntax YYYYMMDD typically
    using LDAP syntax Numstring.
    """
    oid: str = 'NumstringDate-oid'
    desc: str = 'Date in syntax YYYYMMDD'
    pattern = re.compile('^[0-9]{4}[0-1][0-9][0-3][0-9]$')
    storage_format = '%Y%m%d'


class ISO8601Date(Date):
    """
    Plugin class for a date using syntax YYYY-MM-DD (see ISO 8601).
    """
    oid: str = 'ISO8601Date-oid'
    desc: str = 'Date in syntax YYYY-MM-DD (see ISO 8601)'
    pattern = re.compile('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$')
    storage_format = '%Y-%m-%d'


class DateOfBirth(ISO8601Date):
    """
    Plugin class for date of birth syntax YYYY-MM-DD (see ISO 8601).

    Displays the age based at current time.
    """
    oid: str = 'DateOfBirth-oid'
    desc: str = 'Date of birth: syntax YYYY-MM-DD (see ISO 8601)'

    @staticmethod
    def _age(birth_dt):
        birth_date = datetime.date(
            year=birth_dt.year,
            month=birth_dt.month,
            day=birth_dt.day,
        )
        current_date = datetime.date.today()
        age = current_date.year - birth_date.year
        if birth_date.month > current_date.month or \
           (birth_date.month == current_date.month and birth_date.day > current_date.day):
            age = age - 1
        return age

    def _validate(self, attr_value: bytes) -> bool:
        try:
            birth_dt = datetime.datetime.strptime(
                attr_value.decode(self._app.ls.charset),
                self.storage_format
            )
        except ValueError:
            return False
        return self._age(birth_dt) >= 0

    def display(self, vidx, links) -> str:
        raw_date = ISO8601Date.display(self, vidx, links)
        try:
            birth_dt = datetime.datetime.strptime(self.av_u, self.storage_format)
        except ValueError:
            return raw_date
        return '%s (%s years old)' % (raw_date, self._age(birth_dt))


class SecondsSinceEpoch(Integer):
    """
    Plugin class for seconds since epoch (1970-01-01 00:00:00).
    """
    oid: str = 'SecondsSinceEpoch-oid'
    desc: str = 'Seconds since epoch (1970-01-01 00:00:00)'
    min_value = 0

    def display(self, vidx, links) -> str:
        int_str = Integer.display(self, vidx, links)
        try:
            return '%s (%s)' % (
                strftimeiso8601(time.gmtime(float(self._av))),
                int_str,
            )
        except ValueError:
            return int_str


class DaysSinceEpoch(Integer):
    """
    Plugin class for days since epoch (1970-01-01).
    """
    oid: str = 'DaysSinceEpoch-oid'
    desc: str = 'Days since epoch (1970-01-01)'
    min_value = 0

    def display(self, vidx, links) -> str:
        int_str = Integer.display(self, vidx, links)
        try:
            return '%s (%s)' % (
                strftimeiso8601(time.gmtime(float(self._av)*86400)),
                int_str,
            )
        except ValueError:
            return int_str


class Timespan(Integer):
    oid: str = 'Timespan-oid'
    desc: str = 'Time span in seconds'
    input_size: int = LDAPSyntax.input_size
    min_value = 0
    time_divisors = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('mins', 60),
        ('secs', 1),
    )
    sep = ','

    def sanitize(self, attr_value: bytes) -> bytes:
        if not attr_value:
            return attr_value
        try:
            result = repr2ts(
                self.time_divisors,
                self.sep,
                attr_value.decode('ascii')
            ).encode('ascii')
        except ValueError:
            result = Integer.sanitize(self, attr_value)
        return result

    def form_value(self) -> str:
        if not self._av:
            return ''
        try:
            result = ts2repr(self.time_divisors, self.sep, self._av)
        except ValueError:
            result = Integer.form_value(self)
        return result

    def input_field(self) -> web_forms.Field:
        return IA5String.input_field(self)

    def display(self, vidx, links) -> str:
        try:
            result = self._app.form.s2d('%s (%s)' % (
                ts2repr(self.time_divisors, self.sep, self.av_u),
                Integer.display(self, vidx, links)
            ))
        except ValueError:
            result = Integer.display(self, vidx, links)
        return result


class SelectList(DirectoryString):
    """
    Base class for dictionary based select lists which
    should not be used directly
    """
    oid: str = 'SelectList-oid'
    attr_value_dict: Dict[str, str] = {}   # Mapping attribute value to attribute description
    input_fallback: bool = True  # Fallback to normal input field if attr_value_dict is empty
    desc_sep: str = ' '
    tag_tmpl: Dict[bool, str] = {
        False: '{attr_text}: {attr_value}',
        True: '<span title="{attr_title}">{attr_text}:{sep}{attr_value}</span>',
    }

    def get_attr_value_dict(self) -> Dict[str, str]:
        # Enable empty value in any case
        attr_value_dict: Dict[str, str] = {'': '-/-'}
        attr_value_dict.update(self.attr_value_dict)
        return attr_value_dict

    def _sorted_select_options(self):
        # First generate a set of all other currently available attribute values
        fval = DirectoryString.form_value(self)
        # Initialize a dictionary with all options
        vdict = self.get_attr_value_dict()
        # Remove other existing values from the options dict
        for val in self._entry.get(self._at, []):
            val = val.decode(self._app.ls.charset)
            if val != fval:
                try:
                    del vdict[val]
                except KeyError:
                    pass
        # Add the current attribute value if needed
        if fval not in vdict:
            vdict[fval] = fval
        # Finally return the sorted option list
        result = []
        for key, val in vdict.items():
            if isinstance(val, str):
                result.append((key, val, None))
            elif isinstance(val, tuple):
                result.append((key, val[0], val[1]))
        return sorted(
            result,
            key=lambda x: x[1].lower(),
        )

    def _validate(self, attr_value: bytes) -> bool:
        attr_value_dict: Dict[str, str] = self.get_attr_value_dict()
        return attr_value.decode(self._app.ls.charset) in attr_value_dict

    def display(self, vidx, links) -> str:
        attr_value_str = DirectoryString.display(self, vidx, links)
        attr_value_dict: Dict[str, str] = self.get_attr_value_dict()
        try:
            attr_value_desc = attr_value_dict[self.av_u]
        except KeyError:
            return attr_value_str
        try:
            attr_text, attr_title = attr_value_desc
        except ValueError:
            attr_text, attr_title = attr_value_desc, None
        if attr_text == attr_value_str:
            return attr_value_str
        return self.tag_tmpl[bool(attr_title)].format(
            attr_value=attr_value_str,
            sep=self.desc_sep,
            attr_text=self._app.form.s2d(attr_text),
            attr_title=self._app.form.s2d(attr_title or '')
        )

    def input_field(self) -> web_forms.Field:
        attr_value_dict: Dict[str, str] = self.get_attr_value_dict()
        if self.input_fallback and \
           (not attr_value_dict or not list(filter(None, attr_value_dict.keys()))):
            return DirectoryString.input_field(self)
        field = web_forms.Select(
            self._at,
            ': '.join([self._at, self.desc]),
            1,
            options=self._sorted_select_options(),
            default=self.form_value(),
            required=0
        )
        field.charset = self._app.form.accept_charset
        return field


class PropertiesSelectList(SelectList):
    """
    Plugin base class for attribute value select lists of LDAP syntax DirectoryString
    constructed and validated by reading a properties file.
    """
    oid: str = 'PropertiesSelectList-oid'
    properties_pathname: Optional[str] = None
    properties_charset: str = 'utf-8'
    properties_delimiter: str = '='

    def get_attr_value_dict(self) -> Dict[str, str]:
        attr_value_dict: Dict[str, str] = SelectList.get_attr_value_dict(self)
        real_path_name = get_variant_filename(
            self.properties_pathname,
            self._app.form.accept_language
        )
        with open(real_path_name, 'rb') as prop_file:
            for line in prop_file.readlines():
                line = line.decode(self.properties_charset).strip()
                if line and not line.startswith('#'):
                    key, value = line.split(self.properties_delimiter, 1)
                    attr_value_dict[key.strip()] = value.strip()
        return attr_value_dict
        # end of get_attr_value_dict()


class DynamicValueSelectList(SelectList, DirectoryString):
    """
    Plugin base class for attribute value select lists of LDAP syntax DirectoryString
    constructed and validated by internal LDAP search.
    """
    oid: str = 'DynamicValueSelectList-oid'
    ldap_url: Optional[str] = None
    value_prefix: str = ''
    value_suffix: str = ''
    ignored_errors = (
        ldap0.NO_SUCH_OBJECT,
        ldap0.SIZELIMIT_EXCEEDED,
        ldap0.TIMELIMIT_EXCEEDED,
        ldap0.PARTIAL_RESULTS,
        ldap0.INSUFFICIENT_ACCESS,
        ldap0.CONSTRAINT_VIOLATION,
        ldap0.REFERRAL,
    )

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        self.lu_obj = ldap0.ldapurl.LDAPUrl(self.ldap_url)
        self.min_len = len(self.value_prefix)+len(self.value_suffix)
        SelectList.__init__(self, app, dn, schema, attrType, attr_value, entry)

    def _filterstr(self):
        return self.lu_obj.filterstr or '(objectClass=*)'

    def _search_ref(self, attr_value: str):
        attr_value = attr_value[len(self.value_prefix):-len(self.value_suffix) or None]
        search_filter = '(&%s(%s=%s))' % (
            self._filterstr(),
            self.lu_obj.attrs[0],
            attr_value,
        )
        try:
            ldap_result = self._app.ls.l.search_s(
                self._search_root(),
                self.lu_obj.scope,
                search_filter,
                attrlist=self.lu_obj.attrs,
                sizelimit=2,
            )
        except (
                ldap0.NO_SUCH_OBJECT,
                ldap0.CONSTRAINT_VIOLATION,
                ldap0.INSUFFICIENT_ACCESS,
                ldap0.REFERRAL,
                ldap0.SIZELIMIT_EXCEEDED,
                ldap0.TIMELIMIT_EXCEEDED,
            ):
            return None
        # Filter out LDAP referrals
        ldap_result = [
            (sre.dn_s, sre.entry_s)
            for sre in ldap_result
            if isinstance(sre, SearchResultEntry)
        ]
        if ldap_result and len(ldap_result) == 1:
            return ldap_result[0]
        return None

    def _validate(self, attr_value: bytes) -> bool:
        av_u = attr_value.decode(self._app.ls.charset)
        if (
                not av_u.startswith(self.value_prefix) or
                not av_u.endswith(self.value_suffix) or
                len(av_u) < self.min_len or
                (self.max_len is not None and len(av_u) > self.max_len)
            ):
            return False
        return self._search_ref(av_u) is not None

    def display(self, vidx, links) -> str:
        if links and self.lu_obj.attrs:
            ref_result = self._search_ref(self.av_u)
            if ref_result:
                ref_dn, ref_entry = ref_result
                try:
                    attr_value_desc = ref_entry[self.lu_obj.attrs[1]][0]
                except (KeyError, IndexError):
                    display_text, link_html = '', ''
                else:
                    if self.lu_obj.attrs[0].lower() == self.lu_obj.attrs[1].lower():
                        display_text = ''
                    else:
                        display_text = self._app.form.s2d(attr_value_desc+':')
                    if links:
                        link_html = self._app.anchor(
                            'read', '&raquo;',
                            [('dn', ref_dn)],
                        )
                    else:
                        link_html = ''
            else:
                display_text, link_html = '', ''
        else:
            display_text, link_html = '', ''
        return ' '.join((
            display_text,
            DirectoryString.display(self, vidx, links),
            link_html,
        ))

    def _search_root(self) -> str:
        ldap_url_dn = self.lu_obj.dn
        if ldap_url_dn == '_':
            result_dn = str(self._app.naming_context)
        elif ldap_url_dn == '.':
            result_dn = self._dn
        elif ldap_url_dn == '..':
            result_dn = str(self.dn.parent())
        elif ldap_url_dn.endswith(',_'):
            result_dn = ','.join((ldap_url_dn[:-2], str(self._app.naming_context)))
        elif ldap_url_dn.endswith(',.'):
            result_dn = ','.join((ldap_url_dn[:-2], self._dn))
        elif ldap_url_dn.endswith(',..'):
            result_dn = ','.join((ldap_url_dn[:-3], str(self.dn.parent())))
        else:
            result_dn = ldap_url_dn
        if result_dn.endswith(','):
            result_dn = result_dn[:-1]
        return result_dn
        # end of _search_root()

    def get_attr_value_dict(self) -> Dict[str, str]:
        attr_value_dict: Dict[str, str] = SelectList.get_attr_value_dict(self)
        if self.lu_obj.hostport:
            raise ValueError(
                'Connecting to other server not supported! hostport attribute was %r' % (
                    self.lu_obj.hostport
                )
            )
        search_scope = self.lu_obj.scope or ldap0.SCOPE_BASE
        search_attrs = (self.lu_obj.attrs or []) + ['description', 'info']
        # Use the existing LDAP connection as current user
        try:
            ldap_result = self._app.ls.l.search_s(
                self._search_root(),
                search_scope,
                filterstr=self._filterstr(),
                attrlist=search_attrs,
            )
        except self.ignored_errors:
            return {}
        if search_scope == ldap0.SCOPE_BASE:
            # When reading a single entry we build the map from a single multi-valued attribute
            assert len(self.lu_obj.attrs or []) == 1, ValueError(
                'attrlist in ldap_url must be of length 1 if scope is base, got %r' % (
                    self.lu_obj.attrs,
                )
            )
            list_attr = self.lu_obj.attrs[0]
            attr_values_u = [
                ''.join((
                    self.value_prefix,
                    attr_value,
                    self.value_suffix,
                ))
                for attr_value in ldap_result[0].entry_s[list_attr]
            ]
            attr_value_dict: Dict[str, str] = {
                u: u
                for u in attr_values_u
            }
        else:
            if not self.lu_obj.attrs:
                option_value_map, option_text_map = (None, None)
            elif len(self.lu_obj.attrs) == 1:
                option_value_map, option_text_map = (None, self.lu_obj.attrs[0])
            elif len(self.lu_obj.attrs) >= 2:
                option_value_map, option_text_map = self.lu_obj.attrs[:2]
            for sre in ldap_result:
                # Check whether it's a real search result (skip search continuations)
                if not isinstance(sre, SearchResultEntry):
                    continue
                sre.entry_s[None] = [sre.dn_s]
                try:
                    option_value = ''.join((
                        self.value_prefix,
                        sre.entry_s[option_value_map][0],
                        self.value_suffix,
                    ))
                except KeyError:
                    pass
                else:
                    try:
                        option_text = sre.entry_s[option_text_map][0]
                    except KeyError:
                        option_text = option_value
                    option_title = sre.entry_s.get('description', sre.entry_s.get('info', ['']))[0]
                    if option_title:
                        attr_value_dict[option_value] = (option_text, option_title)
                    else:
                        attr_value_dict[option_value] = option_text
        return attr_value_dict
        # end of get_attr_value_dict()


class DynamicDNSelectList(DynamicValueSelectList, DistinguishedName):
    """
    Plugin base class for attribute value select lists of LDAP syntax DN
    constructed and validated by internal LDAP search.
    """
    oid: str = 'DynamicDNSelectList-oid'

    def _get_ref_entry(self, dn: str, attrlist=None) -> dict:
        try:
            sre = self._app.ls.l.read_s(
                dn,
                attrlist=attrlist or self.lu_obj.attrs,
                filterstr=self._filterstr(),
            )
        except (
                ldap0.NO_SUCH_OBJECT,
                ldap0.CONSTRAINT_VIOLATION,
                ldap0.INSUFFICIENT_ACCESS,
                ldap0.INVALID_DN_SYNTAX,
                ldap0.REFERRAL,
            ):
            return None
        if sre is None:
            return None
        return sre.entry_s

    def _validate(self, attr_value: bytes) -> bool:
        return SelectList._validate(self, attr_value)

    def display(self, vidx, links) -> str:
        if links and self.lu_obj.attrs:
            ref_entry = self._get_ref_entry(self.av_u) or {}
            try:
                attr_value_desc = ref_entry[self.lu_obj.attrs[0]][0]
            except (KeyError, IndexError):
                display_text = ''
            else:
                display_text = self._app.form.s2d(attr_value_desc+': ')
        else:
            display_text = ''
        return self.desc_sep.join((
            display_text,
            DistinguishedName.display(self, vidx, links)
        ))


class DerefDynamicDNSelectList(DynamicDNSelectList):
    """
    Plugin base class for attribute value select lists of LDAP syntax DN
    constructed and validated by internal LDAP search.

    Same as DynamicDNSelectList except that Dereference extended control is used.
    """
    oid: str = 'DerefDynamicDNSelectList-oid'

    def _get_ref_entry(self, dn: str, attrlist=None) -> dict:
        deref_crtl = DereferenceControl(
            True,
            {self._at: self.lu_obj.attrs or ['entryDN']}
        )
        try:
            ldap_result = self._app.ls.l.search_s(
                self._dn,
                ldap0.SCOPE_BASE,
                filterstr='(objectClass=*)',
                attrlist=['1.1'],
                req_ctrls=[deref_crtl],
            )[0]
        except (
                ldap0.NO_SUCH_OBJECT,
                ldap0.CONSTRAINT_VIOLATION,
                ldap0.INSUFFICIENT_ACCESS,
                ldap0.INVALID_DN_SYNTAX,
                ldap0.REFERRAL,
            ):
            return None
        if ldap_result is None or not ldap_result.ctrls:
            return None
        for ref in ldap_result.ctrls[0].derefRes[self._at]:
            if ref.dn_s == dn:
                return ref.entry_s
        return None


class Boolean(SelectList, IA5String):
    """
    Plugin class for LDAP syntax 'Boolean'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.3)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.7'
    desc: str = 'Boolean'
    attr_value_dict: Dict[str, str] = {
        'TRUE': 'TRUE',
        'FALSE': 'FALSE',
    }

    def get_attr_value_dict(self) -> Dict[str, str]:
        attr_value_dict: Dict[str, str] = SelectList.get_attr_value_dict(self)
        if self._av and self._av.lower() == self._av:
            for key, val in attr_value_dict.items():
                del attr_value_dict[key]
                attr_value_dict[key.lower()] = val.lower()
        return attr_value_dict

    def _validate(self, attr_value: bytes) -> bool:
        if not self._av and attr_value.lower() == attr_value:
            return SelectList._validate(self, attr_value.upper())
        return SelectList._validate(self, attr_value)

    def display(self, vidx, links) -> str:
        return IA5String.display(self, vidx, links)


class CountryString(SelectList):
    """
    Plugin class for LDAP syntax 'Country String'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.4)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.11'
    desc: str = 'Two letter country string as listed in ISO 3166-2'
    sani_funcs = (
        bytes.strip,
    )

    def get_attr_value_dict(self) -> Dict[str, str]:
        # Enable empty value in any case
        attr_value_dict: Dict[str, str] = {'': '-/-'}
        attr_value_dict.update({
            alpha2: cty.name  for alpha2, cty in iso3166.countries_by_alpha2.items()
        })
        return attr_value_dict


class DeliveryMethod(PrintableString):
    """
    Plugin class for LDAP syntax 'Delivery Method'
    (see https://datatracker.ietf.org/doc/html/rfc4517#section-3.3.5)
    """
    oid: str = '1.3.6.1.4.1.1466.115.121.1.14'
    desc: str = 'Delivery Method'
    pdm = '(any|mhs|physical|telex|teletex|g3fax|g4fax|ia5|videotex|telephone)'
    pattern = re.compile('^%s[ $]*%s$' % (pdm, pdm))


class BitArrayInteger(MultilineText, Integer):
    """
    Plugin class for attributes with Integer syntax where the integer
    value is interpreted as binary flags
    """
    oid: str = 'BitArrayInteger-oid'
    flag_desc_table: Sequence[Tuple[str, int]] = tuple()
    true_false_desc: Dict[bool, str] = {
        False: '-',
        True: '+',
    }

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        Integer.__init__(self, app, dn, schema, attrType, attr_value, entry)
        self.flag_desc2int = dict(self.flag_desc_table)
        self.flag_int2desc = {
            j: i
            for i, j in self.flag_desc_table
        }
        self.max_value = sum([j for i, j in self.flag_desc_table])
        self.min_input_rows = self.max_input_rows = max(len(self.flag_desc_table), 1)

    def sanitize(self, attr_value: bytes) -> bytes:
        try:
            av_u = attr_value.decode('ascii')
        except UnicodeDecodeError:
            return attr_value
        try:
            result = int(av_u)
        except ValueError:
            result = 0
            for row in av_u.split('\n'):
                row = row.strip()
                try:
                    flag_set, flag_desc = row[0:1], row[1:]
                except IndexError:
                    pass
                else:
                    if flag_set == '+':
                        try:
                            result = result | self.flag_desc2int[flag_desc]
                        except KeyError:
                            pass
        return str(result).encode('ascii')

    def form_value(self) -> str:
        attr_value_int = int(self.av_u or 0)
        flag_lines = [
            ''.join((
                self.true_false_desc[int((attr_value_int & flag_int) > 0)],
                flag_desc
            ))
            for flag_desc, flag_int in self.flag_desc_table
        ]
        return '\r\n'.join(flag_lines)

    def input_field(self) -> web_forms.Field:
        fval = self.form_value()
        return web_forms.Textarea(
            self._at,
            ': '.join([self._at, self.desc]),
            self.max_len, self.max_values,
            None,
            default=fval,
            rows=max(self.min_input_rows, min(self.max_input_rows, fval.count('\n'))),
            cols=max([len(desc) for desc, _ in self.flag_desc_table])+1
        )

    def display(self, vidx, links) -> str:
        av_i = int(self._av)
        return (
            '%s<br>'
            '<table summary="Flags">'
            '<tr><th>Property flag</th><th>Value</th><th>Status</th></tr>'
            '%s'
            '</table>'
        ) % (
            Integer.display(self, vidx, links),
            '\n'.join([
                '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                    self._app.form.s2d(desc),
                    hex(flag_value),
                    {False: '-', True: 'on'}[(av_i & flag_value) > 0]
                )
                for desc, flag_value in self.flag_desc_table
            ])
        )


class GSER(DirectoryString):
    """
    Generic String Encoding Rules (GSER) for ASN.1 Types (see RFC 3641)
    """
    oid: str = 'GSER-oid'
    desc: str = 'GSER syntax (see RFC 3641)'


class UUID(IA5String):
    """
    Plugin class for Universally Unique IDentifier (UUID), see RFC 4122
    """
    oid: str = '1.3.6.1.1.16.1'
    desc: str = 'UUID'
    pattern = re.compile(
        '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
    )

    def sanitize(self, attr_value: bytes) -> bytes:
        try:
            return str(uuid.UUID(attr_value.decode('ascii').replace(':', ''))).encode('ascii')
        except ValueError:
            return attr_value


class DNSDomain(IA5String):
    """
    Plugin class for fully-qualified DNS domain names
    """
    oid: str = 'DNSDomain-oid'
    desc: str = 'DNS domain name (see RFC 1035)'
    pattern = re.compile(r'^(\*|[a-zA-Z0-9_-]+)(\.[a-zA-Z0-9_-]+)*$')
    # see https://datatracker.ietf.org/doc/html/rfc2181#section-11
    max_len: int = min(255, IA5String.max_len)
    sani_funcs = (
        bytes.lower,
        bytes.strip,
    )

    def sanitize(self, attr_value: bytes) -> bytes:
        attr_value = IA5String.sanitize(self, attr_value)
        return b'.'.join([
            dc.encode('idna')
            for dc in attr_value.decode(self._app.form.accept_charset).split('.')
        ])

    def form_value(self) -> str:
        try:
            result = '.'.join([
                dc.decode('idna')
                for dc in (self._av or b'').split(b'.')
            ])
        except UnicodeDecodeError:
            result = '!!!snipped because of UnicodeDecodeError!!!'
        return result

    def display(self, vidx, links) -> str:
        if self.av_u != self._av.decode('idna'):
            return '%s (%s)' % (
                IA5String.display(self, vidx, links),
                self._app.form.s2d(self.form_value())
            )
        return IA5String.display(self, vidx, links)


class RFC822Address(DNSDomain, IA5String):
    """
    Plugin class for RFC 822 addresses
    """
    oid: str = 'RFC822Address-oid'
    desc: str = 'RFC 822 mail address'
    pattern = re.compile(r'^[\w@.+=/_ ()-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$')
    html_tmpl = '<a href="mailto:{av}">{av}</a>'

    def __init__(self, app, dn: str, schema, attrType: str, attr_value: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attr_value, entry)

    def form_value(self) -> str:
        if not self._av:
            return IA5String.form_value(self)
        try:
            localpart, domainpart = self._av.rsplit(b'@')
        except ValueError:
            return IA5String.form_value(self)
        dns_domain = DNSDomain(self._app, self._dn, self._schema, None, domainpart)
        return '@'.join((
            localpart.decode(self._app.ls.charset),
            dns_domain.form_value()
        ))

    def sanitize(self, attr_value: bytes) -> bytes:
        try:
            localpart, domainpart = attr_value.rsplit(b'@')
        except ValueError:
            return attr_value
        else:
            return b'@'.join((
                localpart,
                DNSDomain.sanitize(self, domainpart)
            ))


class DomainComponent(DNSDomain):
    """
    Plugin class for a single DNS label
    (see https://datatracker.ietf.org/doc/html/rfc2181#section-11)
    """
    oid: str = 'DomainComponent-oid'
    desc: str = 'DNS domain name component'
    pattern = re.compile(r'^(\*|[a-zA-Z0-9_-]+)$')
    max_len: int = min(63, DNSDomain.max_len)


class JSONValue(PreformattedMultilineText):
    """
    Plugin class used for JSON data (see RFC 8259)
    """
    oid: str = 'JSONValue-oid'
    desc: str = 'JSON data'
    lineSep = b'\n'
    mime_type: str = 'application/json'

    def _validate(self, attr_value: bytes) -> bool:
        try:
            json.loads(attr_value)
        except ValueError:
            return False
        return True

    def _split_lines(self, value):
        try:
            obj = json.loads(value)
        except ValueError:
            return PreformattedMultilineText._split_lines(self, value)
        return PreformattedMultilineText._split_lines(
            self,
            json.dumps(
                obj,
                indent=4,
                separators=(',', ': ')
            ).encode('utf-8')
        )

    def sanitize(self, attr_value: bytes) -> bytes:
        try:
            obj = json.loads(attr_value)
        except ValueError:
            return PreformattedMultilineText.sanitize(self, attr_value)
        return json.dumps(
            obj,
            separators=(',', ':')
        ).encode('utf-8')


class XmlValue(PreformattedMultilineText):
    """
    Plugin class used for XML data
    """
    oid: str = 'XmlValue-oid'
    desc: str = 'XML data'
    lineSep = b'\n'
    mime_type: str = 'text/xml'

    def _validate(self, attr_value: bytes) -> bool:
        if not DEFUSEDXML_AVAIL:
            return PreformattedMultilineText._validate(self, attr_value)
        try:
            defusedxml.ElementTree.XML(attr_value)
        except defusedxml.ElementTree.ParseError:
            return False
        return True


class ASN1Object(Binary):
    """
    Plugin class used for BER-encoded ASN.1 data
    """
    oid: str = 'ASN1Object-oid'
    desc: str = 'BER-encoded ASN.1 data'


class AlgorithmOID(OID):
    """
    This base-class class is used for OIDs of cryptographic algorithms
    """
    oid: str = 'AlgorithmOID-oid'


class HashAlgorithmOID(SelectList, AlgorithmOID):
    """
    Plugin class for selection of OIDs for hash algorithms
    (see https://www.iana.org/assignments/hash-function-text-names/).
    """
    oid: str = 'HashAlgorithmOID-oid'
    desc: str = 'values from https://www.iana.org/assignments/hash-function-text-names/'
    attr_value_dict: Dict[str, str] = {
        '1.2.840.113549.2.2': 'md2',          # [RFC3279]
        '1.2.840.113549.2.5': 'md5',          # [RFC3279]
        '1.3.14.3.2.26': 'sha-1',             # [RFC3279]
        '2.16.840.1.101.3.4.2.4': 'sha-224',  # [RFC4055]
        '2.16.840.1.101.3.4.2.1': 'sha-256',  # [RFC4055]
        '2.16.840.1.101.3.4.2.2': 'sha-384',  # [RFC4055]
        '2.16.840.1.101.3.4.2.3': 'sha-512',  # [RFC4055]
    }


class HMACAlgorithmOID(SelectList, AlgorithmOID):
    """
    Plugin class for selection of OIDs for HMAC algorithms (see RFC 8018).
    """
    oid: str = 'HMACAlgorithmOID-oid'
    desc: str = 'values from RFC 8018'
    attr_value_dict: Dict[str, str] = {
        # from RFC 8018
        '1.2.840.113549.2.7': 'hmacWithSHA1',
        '1.2.840.113549.2.8': 'hmacWithSHA224',
        '1.2.840.113549.2.9': 'hmacWithSHA256',
        '1.2.840.113549.2.10': 'hmacWithSHA384',
        '1.2.840.113549.2.11': 'hmacWithSHA512',
    }


class ComposedAttribute(LDAPSyntax):
    """
    This mix-in plugin class composes attribute values from other attribute values.

    One can define an ordered sequence of string templates in class
    attribute ComposedDirectoryString.compose_templates.
    See examples in module web2ldap.app.plugins.inetorgperson.

    Obviously this only works for single-valued attributes,
    more precisely only the "first" attribute value is used.
    """
    oid: str = 'ComposedDirectoryString-oid'
    compose_templates: Sequence[str] = ()

    class SingleValueDict(dict):
        """
        dictionary-like class which only stores and returns the
        first value of an attribute value list
        """

        def __init__(self, entry, encoding):
            dict.__init__(self)
            self._encoding = encoding
            entry = entry or {}
            for key, val in entry.items():
                self.__setitem__(key, val)

        def __setitem__(self, key, val):
            if val and val[0]:
                dict.__setitem__(self, key, val[0].decode(self._encoding))

    def form_value(self) -> str:
        """
        Return a dummy value that attribute is returned from input form and
        then seen by .transmute()
        """
        return ''

    def transmute(self, attr_values: List[bytes]) -> List[bytes]:
        """
        always returns a list with a single value based on the first
        successfully applied compose template
        """
        entry = self.SingleValueDict(self._entry, encoding=self._app.ls.charset)
        for template in self.compose_templates:
            try:
                attr_values = [template.format(**entry).encode(self._app.ls.charset)]
            except KeyError:
                continue
            else:
                break
        else:
            return attr_values
        return attr_values

    def input_field(self) -> web_forms.Field:
        """
        composed attributes must only have hidden input field
        """
        input_field = web_forms.HiddenInput(
            self._at,
            ': '.join([self._at, self.desc]),
            self.max_len,
            self.max_values,
            None,
            default=self.form_value(),
        )
        input_field.charset = self._app.form.accept_charset
        return input_field


class LDAPv3ResultCode(SelectList):
    """
    Plugin base class for attributes with Integer syntax
    constrained to valid LDAP result code.
    """
    oid: str = 'LDAPResultCode-oid'
    desc: str = 'LDAPv3 declaration of resultCode in (see RFC 4511)'
    attr_value_dict: Dict[str, str] = {
        '0': 'success',
        '1': 'operationsError',
        '2': 'protocolError',
        '3': 'timeLimitExceeded',
        '4': 'sizeLimitExceeded',
        '5': 'compareFalse',
        '6': 'compareTrue',
        '7': 'authMethodNotSupported',
        '8': 'strongerAuthRequired',
        '9': 'reserved',
        '10': 'referral',
        '11': 'adminLimitExceeded',
        '12': 'unavailableCriticalExtension',
        '13': 'confidentialityRequired',
        '14': 'saslBindInProgress',
        '16': 'noSuchAttribute',
        '17': 'undefinedAttributeType',
        '18': 'inappropriateMatching',
        '19': 'constraintViolation',
        '20': 'attributeOrValueExists',
        '21': 'invalidAttributeSyntax',
        '32': 'noSuchObject',
        '33': 'aliasProblem',
        '34': 'invalidDNSyntax',
        '35': 'reserved for undefined isLeaf',
        '36': 'aliasDereferencingProblem',
        '48': 'inappropriateAuthentication',
        '49': 'invalidCredentials',
        '50': 'insufficientAccessRights',
        '51': 'busy',
        '52': 'unavailable',
        '53': 'unwillingToPerform',
        '54': 'loopDetect',
        '64': 'namingViolation',
        '65': 'objectClassViolation',
        '66': 'notAllowedOnNonLeaf',
        '67': 'notAllowedOnRDN',
        '68': 'entryAlreadyExists',
        '69': 'objectClassModsProhibited',
        '70': 'reserved for CLDAP',
        '71': 'affectsMultipleDSAs',
        '80': 'other',
    }


class SchemaDescription(DirectoryString):
    oid: str = 'SchemaDescription-oid'
    schema_cls = None
    sani_funcs = (
        bytes.strip,
    )

    def _validate(self, attr_value: bytes) -> bool:
        if self.schema_cls is None:
            return DirectoryString._validate(self, attr_value)
        try:
            _ = self.schema_cls(attr_value.decode(self._app.ls.charset))
        except (IndexError, ValueError):
            return False
        return True


class ObjectClassDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.37'
    schema_cls = ldap0.schema.models.ObjectClass


class AttributeTypeDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.3'
    schema_cls = ldap0.schema.models.AttributeType


class MatchingRuleDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.30'
    schema_cls = ldap0.schema.models.MatchingRule


class MatchingRuleUseDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.31'
    schema_cls = ldap0.schema.models.MatchingRuleUse


class LDAPSyntaxDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.54'
    schema_cls = ldap0.schema.models.LDAPSyntax


class DITContentRuleDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.16'
    schema_cls = ldap0.schema.models.DITContentRule


class DITStructureRuleDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.17'
    schema_cls = ldap0.schema.models.DITStructureRule


class NameFormDescription(SchemaDescription):
    oid: str = '1.3.6.1.4.1.1466.115.121.1.35'
    schema_cls = ldap0.schema.models.NameForm


# Set up the central syntax registry instance
syntax_registry = SyntaxRegistry()

# Register all syntax classes in this module
syntax_registry.reg_syntaxes(__name__)
